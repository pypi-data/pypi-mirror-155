'''ZCC Controller Class.'''
from __future__ import annotations

import asyncio
from pprint import pformat
import logging
import re
import socket
from typing import Dict, List
import uuid

from zcc.constants import LEVEL_BY_VERBOSITY, NAME, VERSION
from zcc.description import ControlPointDescription
from zcc.device import ControlPointDevice
from zcc.errors import ControlPointError
from zcc.socket import ControlPointSocket
from zcc.protocol import ControlPointProtocol
from zcc.watchdog import ControlPointWatchdog


class ControlPoint:
    '''Represents the ZCC controller which connects to individual devices'''

    def __init__(self, description: ControlPointDescription = None,
                 timeout: int = 2, verbosity: int = 0):

        self.logger = logging.getLogger('ControlPoint')
        if verbosity > 2:
            verbosity = 2
        self.logger.setLevel(LEVEL_BY_VERBOSITY[verbosity])

        self.host = description.host
        self.port = description.port

        if not (self.host and self.port):
            raise ControlPointError(
                'ControlPoint initialisation failed - must provide at least host and port.')

        self.logger.info(
            'Setting up %s version %s', NAME, VERSION)

        self.brand = description.brand
        self.product = description.product
        self.mac = description.mac
        self.available_tcps = description.available_tcps

        self.timeout = timeout
        self.verbosity = verbosity

        self.devices: Dict[ControlPointDevice] = {}

        self.actions_received = 0
        self.properties_received = 0
        self.states_received = 0

        self.device_mac = format(uuid.getnode(), '=012x')
        self.access_token = None
        self.authorised = False
        self.session_started = False

        self.socket = None
        self.closed_socket = None

        self.ready = False

        self.loop = asyncio.get_event_loop()
        self.authorised: asyncio.Future = None
        self.session_started: asyncio.Future = None
        self.properties_ready: asyncio.Future = None
        self.actions_ready: asyncio.Future = None
        self.states_ready: asyncio.Future = None

        self.connected_ready = asyncio.Event()

        self.watchdog_timer: ControlPointWatchdog = None

    @ property
    def doors(self) -> List[ControlPointDevice]:
        '''Return an array with all doors'''
        return list(filter(lambda device: device.type == 'garagedoor', self.devices.values()))

    @ property
    def fans(self) -> List[ControlPointDevice]:
        '''Return an array with all fans'''
        return list(filter(lambda device: device.type == 'fan', self.devices.values()))

    @ property
    def lights(self) -> List[ControlPointDevice]:
        '''Return an array with all lights (i.e. switch or dimmer type)'''
        return list(filter(lambda device:
                           device.type == 'light' or
                           device.type == 'switch' or
                           device.type == 'dimmer', self.devices.values()))

    @ property
    def outlets(self) -> List[ControlPointDevice]:
        '''Return an array with all outlets'''
        return list(filter(lambda device: device.type == 'outlet', self.devices.values()))

    @ property
    def sensors(self) -> List[ControlPointDevice]:
        '''Return an array with all sensors'''
        return list(filter(lambda device: device.type == 'garagedoor', self.devices.values()))

    async def connect(self, fast: bool = False) -> bool:
        '''Connect to ZCC, build device table and subscribe to updates'''
        self.logger.info('Connecting to ZCC %s:%d', self.host, self.port)

        self.connected_ready.clear()

        if self.authorised:
            self.authorised.cancel()
        self.authorised = self.loop.create_future()

        if self.session_started:
            self.session_started.cancel()
        self.session_started = self.loop.create_future()

        if not self.socket:
            self.socket = ControlPointSocket(
                self.host, self.port, timeout=self.timeout, verbosity=self.verbosity)

        try:
            await self.socket.connect()
        except ConnectionRefusedError as error:
            description = f'Connection refused when connecting to ZCC {self.host}:{self.port}'
            self.logger.error('connect() %s', description)
            raise ControlPointError(description) from error
        except socket.error as error:
            description = f'Socket error when connecting to ZCC {self.host}:{self.port}'
            self.logger.error('connect() %s', description)
            raise ControlPointError(description) from error
        except Exception as error:
            raise ControlPointError(
                'Unknown error when connecting to ZCC') from error

        self.socket.subscribe(self)

        await self.socket.sendall(ControlPointProtocol.authorise(self.device_mac),
                                  response_expected=False)

        try:
            self.logger.info('connect() waiting for authorisation')
            await asyncio.wait_for(self.authorised,
                                   timeout=ControlPointProtocol.AUTH_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            self.logger.error('connect() timeout waiting for authorisation')
            raise ControlPointError(
                "Unable to authorise connection to ZCC.") from error

        await self.socket.sendall(ControlPointProtocol.start(
            self.device_mac, self.access_token), response_expected=False)

        try:
            self.logger.info('connect() waiting for session start')
            await asyncio.wait_for(self.session_started,
                                   timeout=ControlPointProtocol.START_SESSION_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            self.logger.error('connect() timeout waiting for session start')
            raise ControlPointError(
                "Unable to start session.") from error

        if not fast:
            await self.__get_devices()

        await self.socket.sendall(ControlPointProtocol.subscribe(), response_expected=False)

        await asyncio.sleep(ControlPointProtocol.SUBSCRIBE_TIMEOUT)

        self.ready = True

        self.connected_ready.set()

        self.logger.info('Connected to ZCC %s:%d with %d/%d/%d actions/properties/states',
                         self.host, self.port,
                         self.actions_received, self.states_received, self.properties_received)

    def __del__(self):
        self.disconnect()

    def describe(self) -> str:
        '''Return a string representation of ZCC including devices'''
        header = '+' + '-' * 130 + '+'
        if self.host:
            description = header + '\n'
            description += '| ControlPoint: %12s        %8s %8s %27s devices        %16s:%-6d %s Tcps    |\n' % (
                self.mac if self.mac else "n/a",
                self.product if self.product else 'n/a',
                self.brand if self.brand else 'n/a',
                str(len(self.devices)),
                self.host,
                self.port,
                str(self.available_tcps) if self.available_tcps else "n/a")
            description += header + '\n'
            for key in self.devices:
                description += self.devices[key].describe()
            return description
        else:
            return 'ControlPoint: not found'

    def disconnect(self):
        '''Disconnect from zimi controller'''
        # await self.socket.sendall(ControlPointProtocol.unsubscribe())
        self.socket.unsubscribe(self)

    async def __get_devices(self):
        '''Get initial device data from controller.'''

        self.properties_ready = self.loop.create_future()
        self.actions_ready = self.loop.create_future()
        self.states_ready = self.loop.create_future()

        self.logger.info('__get_devices() getting properties')
        await self.socket.sendall(ControlPointProtocol.get('properties'), response_expected=False)

        try:
            await asyncio.wait_for(self.properties_ready,
                                   timeout=ControlPointProtocol.DEVICE_GET_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            raise ControlPointError(
                "ZCC connection failed - didn't receive any properties.") from error

        await asyncio.sleep(ControlPointProtocol.DEVICE_GET_TIMEOUT)

        self.logger.info('__get_devices() getting actions')
        await self.socket.sendall(ControlPointProtocol.get('actions'), response_expected=False)

        try:
            await asyncio.wait_for(self.actions_ready,
                                   timeout=ControlPointProtocol.DEVICE_GET_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            raise ControlPointError(
                "ZCC connection failed - didn't receive any actions.") from error

        await asyncio.sleep(ControlPointProtocol.DEVICE_GET_TIMEOUT)

        self.logger.info('__get_devices() getting states')
        await self.socket.sendall(ControlPointProtocol.get('states'), response_expected=False)

        try:
            await asyncio.wait_for(self.states_ready,
                                   timeout=ControlPointProtocol.DEVICE_GET_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            raise ControlPointError(
                "ZCC connection failed - didn't receive any states.") from error

        await asyncio.sleep(ControlPointProtocol.DEVICE_GET_TIMEOUT)

    async def __get_states(self):
        '''Get latest state data from controller and reset watchdog.'''

        self.states_ready = self.loop.create_future()

        self.logger.info('__get_states() getting states')
        await self.socket.sendall(ControlPointProtocol.get('states'))

        try:
            await asyncio.wait_for(self.states_ready,
                                   timeout=ControlPointProtocol.DEVICE_GET_TIMEOUT)
        except asyncio.exceptions.TimeoutError as error:
            raise ControlPointError(
                "ZCC connection failed - didn't receive updated states.") from error

        if self.watchdog_timer:
            self.watchdog_timer.reset()

    def print_description(self):
        '''Print description of the ZCC controller.'''
        print(self.describe())

    async def notify(self, notifier):
        '''Receive a notification of an updated object.
        Pull the data off the queue.   If None is received then
        assume the socket has been closed and needs re-opening.'''

        response = notifier.get()

        if not response:
            await self.re_connect()
            return

        self.logger.debug('notify() received:\n%s', response)

        if response.get(ControlPointProtocol.AUTH_APP_FAILED, None):
            self.logger.info("Authorisation failed\n%s", pformat(response))
        if response.get(ControlPointProtocol.AUTH_APP_SUCCESS, None):
            self.logger.info("Authorisation success\n%s", pformat(response))
            self.access_token = response[ControlPointProtocol.AUTH_APP_SUCCESS]['accessToken']
            self.authorised.set_result(True)
        if response.get(ControlPointProtocol.START_SESSION_FAILED, None):
            self.logger.info("Start session failed\n%s", pformat(response))
        if response.get(ControlPointProtocol.START_SESSION_SUCCESS, None):
            self.logger.info("Start session success\n%s", pformat(response))
            self.session_started.set_result(True)
        if response.get(ControlPointProtocol.CONTROLPOINT_ACTIONS, None):
            self.__update_devices(response.get(
                ControlPointProtocol.CONTROLPOINT_ACTIONS, None), 'actions')
        if response.get(ControlPointProtocol.CONTROLPOINT_PROPERTIES, None):
            self.__update_devices(response.get(
                ControlPointProtocol.CONTROLPOINT_PROPERTIES, None), 'properties')
        if response.get(ControlPointProtocol.CONTROLPOINT_STATES, None):
            self.__update_devices(response.get(
                ControlPointProtocol.CONTROLPOINT_STATES, None), 'states')
        if response.get(ControlPointProtocol.CONTROLPOINT_STATES_EVENTS, None):
            self.__update_devices(response.get(
                ControlPointProtocol.CONTROLPOINT_STATES_EVENTS, None), 'states')

    async def re_connect(self):
        '''Re-connect to a new socket and resend any queued messages.'''

        self.logger.error('Existing socket closed - reconnecting to ZCC')

        self.socket.unsubscribe(self)

        self.closed_socket = self.socket
        self.socket = None

        self.ready = False

        while not self.ready:

            try:
                self.logger.info('re_connect() starting connect')
                await self.connect(fast=True)

                while True:
                    message = self.closed_socket.unsent()
                    if message:
                        self.logger.error(
                            'Re-sending message:\n%s', message)
                        await self.socket.sendall(message)
                    else:
                        break
            except ControlPointError as error:
                self.logger.error(
                    "re_connect() failed with ControlPointError %s - will retry in %d",
                    error, ControlPointProtocol.RETRY_TIMEOUT)
                await asyncio.sleep(ControlPointProtocol.RETRY_TIMEOUT)

        self.closed_socket.close()
        self.closed_socket = None

        if self.watchdog_timer:
            self.watchdog_timer.reset()

    async def set(self, identifier: str, action: str, params: object = None):
        '''Sends an action for a device.'''

        while not self.connected_ready.is_set():
            self.logger.error('set() not ready - attempting to connect')
            try:
                await self.re_connect()
            except ControlPointError as error:
                self.logger.error('set() connection failed - trying again')

        # await self.connected_ready.wait()

        message = ControlPointProtocol.set(identifier, action, params)
        success = False
        while not success:
            success = await self.socket.sendall(message)
            self.logger.info("Sending %s request to %s (%s)",
                             action, self.devices[identifier].location, identifier)

    def __str__(self):
        return pformat(vars(self)) + '\n'

    def start_watchdog(self, timer: int):
        '''Start a periodic timeout that resets every time a status update is received.'''

        if self.watchdog_timer:
            self.stop_watchdog()

        self.logger.info("Starting Watchdog for %s seconds", timer)
        self.watchdog_timer = ControlPointWatchdog(
            timer, self.trigger_watchdog)
        self.watchdog_timer.start()

    def stop_watchdog(self):
        '''Stop the periodic timeout.'''

        self.logger.info("Stopping existing Watchdog")

        if self.watchdog_timer:
            self.watchdog_timer.cancel()
            self.watchdog_timer = None

    async def trigger_watchdog(self):
        '''Trigger the watchdog function - which will reset the connection.'''
        # self.logger.error(
        #     "Triggering the watchdog timer - will initiate re-connection")
        # await self.re_connect()
        self.logger.error(
            "Triggering the watchdog timer - will fetch new states")
        await self.__get_states()

    def __update_devices(self, devices, target):
        '''Update device target with JSON data for all devices.'''

        for device in devices:
            updates_made = False
            identifier = device['id']
            if not self.devices.get(identifier):
                self.devices[identifier] = ControlPointDevice(self, identifier)
            if 'actions' in target and self.devices[identifier].actions != device[target]:
                self.devices[identifier].actions = device[target]
                self.actions_received += 1
                updates_made = True
            if 'properties' in target and self.devices[identifier].properties != device[target]:
                self.devices[identifier].properties = device[target]
                self.properties_received += 1
                updates_made = True
            if 'states' in target and self.devices[identifier].states != device[target]:
                self.devices[identifier].states = device[target]
                self.states_received += 1
                updates_made = True
            if updates_made:
                if self.watchdog_timer:
                    self.watchdog_timer.reset()
                if self.ready:
                    self.logger.info(
                        'Received %s update for %s (%s):\n%s',
                        target, self.devices[identifier].location, identifier, device[target])
                else:
                    self.logger.debug(
                        'Received %s update for %s (%s):\n%s',
                        target, self.devices[identifier].location, identifier, device[target])
                self.devices[identifier].notify_observers()

        if self.actions_received > 0 and not self.actions_ready.done():
            self.actions_ready.set_result(True)
        if self.properties_received > 0 and not self.properties_ready.done():
            self.properties_ready.set_result(True)
        if self.states_received > 0 and not self.states_ready.done():
            self.states_ready.set_result(True)

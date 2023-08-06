'''ZCC Discovery Service Class'''
from __future__ import annotations

import asyncio
import json
from json.decoder import JSONDecodeError
import logging
import socket
from typing import Tuple

from zcc.constants import LEVEL_BY_VERBOSITY
from zcc.description import ControlPointDescription
from zcc.errors import ControlPointError
from zcc.protocol import ControlPointProtocol


class ControlPointDiscoveryProtocol(asyncio.DatagramProtocol):
    '''Listens for ZCC announcements on the defined UDP port.'''

    def __init__(self, discovery_complete: asyncio.Future, discovery_result: object) -> None:
        super().__init__()
        self.discovery_complete: asyncio.Future = discovery_complete
        self.discovery_result = discovery_result
        self.transport: asyncio.transports.DatagramTransport = None
        self.logger = logging.getLogger('ControlPointDiscoveryService')

    def connection_lost(self, exc) -> None:
        self.transport.close()
        return super().connection_lost(exc)

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        self.transport = transport
        return super().connection_made(transport)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:

        data = str(data.decode('UTF-8'))
        self.logger.debug(
            'datagram_received() from %s\n%s', str(addr), data)

        lines = data.split('\n')
        for line in lines:
            try:
                response = json.loads(line)
                if response:
                    self.discovery_result.brand = response['brand']
                    self.discovery_result.product = response['product']
                    self.discovery_result.mac = response['mac']
                    self.discovery_result.host = addr[0]
                    self.discovery_result.port = response['tcp']
                    self.discovery_result.available_tcps = response['availableTcps']
                    self.discovery_complete.set_result(True)
            except JSONDecodeError:
                break

        return super().datagram_received(data, addr)


class ControlPointDiscoveryService:
    '''Provides a ZCC discovery service to discover ZIMI controllers on the local LAN.'''

    def __init__(self, verbosity: int = 0):

        self.logger = logging.getLogger('ControlPointDiscoveryService')
        if verbosity > 2:
            verbosity = 2
        self.logger.setLevel(LEVEL_BY_VERBOSITY[verbosity])

        self.loop = asyncio.get_event_loop()
        self.discovery_complete = self.loop.create_future()
        self.discovery_result = ControlPointDescription()

    async def discover(self) -> ControlPointDescription:
        '''Discover local ZIMI controllers on LAN and return (host,port).'''

        transport, _ = await self.loop.create_datagram_endpoint(
            lambda: ControlPointDiscoveryProtocol(
                self.discovery_complete, self.discovery_result),
            local_addr=('0.0.0.0', ControlPointProtocol.UDP_RECV_PORT))

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        server_address = ('255.255.255.255',
                          ControlPointProtocol.UDP_SEND_PORT)
        message = ControlPointProtocol.discover()

        send_socket.sendto(message.encode(), server_address)
        self.logger.info('Sending discovery message on local network')

        try:
            await asyncio.wait_for(self.discovery_complete, timeout=10)
            self.logger.info("Success - discovered ZIMI controller at %s port %d\n%s",
                             self.discovery_result.host,
                             self.discovery_result.port,
                             self.discovery_result)
            transport.close()
            return self.discovery_result
        except asyncio.exceptions.TimeoutError as error:
            raise ControlPointError(
                "Failure - Unable to discover ZCC by UDP broadcast.") from error

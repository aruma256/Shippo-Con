import asyncio

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer


class OSCValueProvider:
    ADDRESS_SHIPPOCON = "/avatar/parameters/ShippoCon"
    ADDRESS_BEACON_L = f"{ADDRESS_SHIPPOCON}/Beacon/L"
    ADDRESS_BEACON_R = f"{ADDRESS_SHIPPOCON}/Beacon/R"

    def __init__(self) -> None:
        self.beacon_L: float = 0.0
        self.beacon_R: float = 0.0

    def _beacon_callback_L(self, address: str, value: float) -> None:
        self.beacon_L = value

    def _beacon_callback_R(self, address: str, value: float) -> None:
        self.beacon_R = value

    def _build_dispatcher(self) -> Dispatcher:
        dispatcher = Dispatcher()
        dispatcher.map(
            "/avatar/parameters/ShippoCon/Beacon/L",
            self._beacon_callback_L,
        )
        dispatcher.map(
            "/avatar/parameters/ShippoCon/Beacon/R",
            self._beacon_callback_R,
        )
        return dispatcher

    async def start(self, ip: str, port: int) -> None:
        server = AsyncIOOSCUDPServer(
            (ip, port),
            self._build_dispatcher(),
            asyncio.get_event_loop(),
        )
        self._transport, protocol = await server.create_serve_endpoint()

    def stop(self) -> None:
        self._transport.close()

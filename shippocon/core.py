from .jcon import Jcon


class Core:
    def __init__(self) -> None:
        self._jcon_L = Jcon("L")
        self._jcon_R = Jcon("R")

    async def connect_L(self) -> bool:
        return await self._jcon_L.connect()

    async def connect_R(self) -> bool:
        return await self._jcon_R.connect()

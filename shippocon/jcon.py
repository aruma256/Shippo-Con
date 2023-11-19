import asyncio

import hid


VENDOR_ID = 1406
PRODUCT_ID_L = 8198
PRODUCT_ID_R = 8199


class Jcon:
    STATUS_DATA_PACKET_LENGTH = 49

    def __init__(self, side: str) -> None:
        self._device: hid.device | None = None
        self._packet_id = 0
        self._side = side
        assert self._side in {"L", "R"}

    async def connect(self) -> bool:
        if not self._find_device():
            return False
        await self._setup_device()
        return True

    def read_gyro(self) -> tuple[int, int]:
        assert self._device is not None
        status_data_packet = self._device.read(Jcon.STATUS_DATA_PACKET_LENGTH)
        return (
            Jcon.prase_gyro_data(*status_data_packet[19:19+2]),  # X
            Jcon.prase_gyro_data(*status_data_packet[21:21+2]),  # Y
        )

    def _find_device(self) -> bool:
        device = hid.device()
        try:
            device.open(
                VENDOR_ID,
                PRODUCT_ID_L if self._side == "L" else PRODUCT_ID_R,
            )
            self._device = device
            return True
        except OSError:
            return False

    async def _setup_device(self) -> None:
        self._send_subcommand(0x40, 0x01)  # enable IMU data
        await asyncio.sleep(0.1)
        self._send_subcommand(0x48, 0x01)  # enable vibration
        await asyncio.sleep(0.1)
        self._send_subcommand(0x03, 0x30)  # set input report mode

    def _send_subcommand(self,
                         subcommand_number: int,
                         subcommand_arg: int,
                         ) -> None:
        packet = self._create_subcommand_packet(subcommand_number,
                                                subcommand_arg)
        self._send(packet)

    def _create_subcommand_packet(self,
                                  subcommand_number: int,
                                  subcommand_arg: int,
                                  ) -> list[int]:
        packet = [0x01, self._next_packet_id()]
        packet.extend(self._create_rumble_part(0))
        packet.append(subcommand_number)
        packet.append(subcommand_arg)
        return packet

    def _send_rumble(self, rumble_level: int) -> None:
        packet = self._create_rumble_packet(rumble_level)
        self._send(packet)

    def _create_rumble_packet(self, rumble_level: int) -> list[int]:
        packet = [0x10, self._next_packet_id()]
        packet.extend(self._create_rumble_part(rumble_level))
        return packet

    def _create_rumble_part(self, rumble_level: int) -> list[int]:
        assert 0 <= rumble_level <= 11
        rumble_code = (12 - rumble_level) << 2
        rumble_part = [1, 0, rumble_code, 0] * 2
        return rumble_part

    def _next_packet_id(self) -> int:
        current_id = self._packet_id
        self._packet_id = (current_id + 1) % 0x10
        return current_id

    def _send(self, packet: list[int]) -> None:
        assert self._device is not None
        self._device.write(packet)

    @staticmethod
    def prase_gyro_data(first: int, second: int) -> int:
        res = (second << 8) | first
        if second & 0b10000000:
            res -= 1 << 16
        return res

import asyncio
from unittest.mock import Mock

import pytest

from shippocon.jcon import Jcon


VENDOR_ID = 1406
PRODUCT_ID_L = 8198


def test_init():
    with pytest.raises(AssertionError):
        Jcon("X")
    Jcon("L")
    Jcon("R")


def test_read_gyro():
    packet = [0] * Jcon.STATUS_DATA_PACKET_LENGTH
    jcon = Jcon("L")
    jcon._device = device_mock = Mock()
    device_mock.read.return_value = packet

    packet[19] = 0x12
    packet[20] = 0x34
    packet[21] = 0x56
    packet[22] = 0x78
    assert jcon.read_gyro() == (Jcon.prase_gyro_data(0x12, 0x34),
                                Jcon.prase_gyro_data(0x56, 0x78))


def test__create_subcommand_packet():
    jcon = Jcon("L")
    expected = [0x01, 0] + jcon._create_rumble_part(0) + [0x12, 0x34]
    assert jcon._create_subcommand_packet(0x12, 0x34) == expected


@pytest.mark.parametrize('rumble_level, expected_packet', [
    (11, [0x10, 0] + [1, 0, 0b100, 0] * 2),  # max rumble level
    (5, [0x10, 0] + [1, 0, 0b011100, 0] * 2),  # half rumble level
    (0, [0x10, 0] + [1, 0, 0b110000, 0] * 2),  # min rumble level
])
def test__create_rumble_packet(rumble_level, expected_packet):
    jcon = Jcon("L")
    assert jcon._create_rumble_packet(rumble_level) == expected_packet


def test_next_packet_id():
    jcon = Jcon("L")
    assert jcon._next_packet_id() == 0
    assert jcon._next_packet_id() == 1
    jcon._packet_id = 15
    assert jcon._next_packet_id() == 15
    assert jcon._next_packet_id() == 0


@pytest.mark.asyncio
async def test_rumble_with_real_device():
    jcon = Jcon("L")
    if not await jcon.connect():
        pytest.skip("Jcon not found")
    for _ in range(2):
        for i in range(11):
            jcon._send_rumble(i)
            await asyncio.sleep(0.1)


@pytest.mark.asyncio
async def test_gyro_with_real_device():
    jcon = Jcon("L")
    if not await jcon.connect():
        pytest.skip("Jcon not found")
    for _ in range(10*5):
        res = jcon._device.read(Jcon.STATUS_DATA_PACKET_LENGTH)
        print(Jcon.prase_gyro_data(res[19], res[20]))  # X
        # print(Jcon.prase_gyro_data(res[21], res[22]))  # Y
        # print(Jcon.prase_gyro_data(res[23], res[24]))  # Z
        await asyncio.sleep(0.1)

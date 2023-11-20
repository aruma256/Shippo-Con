import asyncio

import pytest
from pythonosc import udp_client

from shippocon.osc_value_provider import OSCValueProvider


@pytest.mark.asyncio
async def test_start():
    provider = OSCValueProvider()
    ip = "127.0.0.1"
    port = 12345
    try:
        await provider.start(ip, port)

        client = udp_client.SimpleUDPClient(ip, port)
        client.send_message(OSCValueProvider.ADDRESS_BEACON_L, 0.5)
        client.send_message(OSCValueProvider.ADDRESS_BEACON_R, -0.5)

        await asyncio.sleep(0.1)
        assert provider.beacon_L == 0.5
        assert provider.beacon_R == -0.5
    finally:
        provider.stop()

from unittest.mock import Mock

from shippocon.tail_position_calculator import TailPositionCalculator


def test():
    provider = Mock()
    provider.beacon_L = 0.75
    provider.beacon_R = 0.25
    calculator = TailPositionCalculator(provider)
    calculator.update()
    assert calculator.get_position() == 0.5

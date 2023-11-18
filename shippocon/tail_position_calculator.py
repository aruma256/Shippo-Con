from .osc_value_provider import OSCValueProvider


class TailPositionCalculator:
    def __init__(self, osc_value_provider: OSCValueProvider) -> None:
        self._osc_value_provider = osc_value_provider
        self._position = 0.

    def update(self) -> None:
        left = self._osc_value_provider.beacon_L
        right = self._osc_value_provider.beacon_R
        self._position = left - right

    def get_position(self) -> float:
        return self._position

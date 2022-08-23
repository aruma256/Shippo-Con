import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

from shippo_con.engine.engine import Engine
from shippo_con.engine.engine_params import EngineParams


class TestEngine:

    def test_reset(self):
        engine = Engine()
        engine._raw_pos = np.array([100000., 100000.])
        engine._xy_abs_max = np.array([100000., 100000.])
        engine.reset()
        assert_array_equal(
            engine._raw_pos,
            np.array([0., 0.])
        )
        assert_array_equal(
            engine._xy_abs_max,
            np.array([1., 1.])
        )

    def test_update(self):
        engine = Engine(EngineParams(decay_factor=0.8))
        engine._raw_pos = np.array([-10., 20.])
        engine.update(np.array([0.2, -0.1]))
        assert_allclose(
            engine._raw_pos,
            np.array([-10*0.8 + 0.2, 20*0.8 - 0.1])
        )

    def test_calc_pos(self):
        engine = Engine()
        engine._raw_pos = np.array([2.5, -2.])
        engine._xy_abs_max = np.array([10., 4.])
        assert_allclose(
            engine.calc_pos(),
            np.array([0.25, -0.5])
        )

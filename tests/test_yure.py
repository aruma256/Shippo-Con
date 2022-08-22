import numpy as np
from numpy.testing import assert_array_equal, assert_allclose

from shippo_con.yure import Yure

class TestYure:

    def test_reset(self):
        yure = Yure()
        yure._raw_pos = np.array([5., 5.])
        yure._xy_abs_max = np.array([6., 6.])
        yure.reset()
        assert_array_equal(yure._raw_pos, np.array([0., 0.]))
        assert_array_equal(yure._xy_abs_max, np.array([1., 1.]))

    def test_update(self):
        yure = Yure()
        yure._raw_pos = np.array([-10., 20.])
        yure.update(np.array([0.2, -0.1]))
        assert_allclose(yure._raw_pos, np.array([-10*0.99 + 0.2, 20*0.99 - 0.1]))

    def test_calc_pos(self):
        yure = Yure()
        yure._raw_pos = np.array([4., -2.])
        yure._xy_abs_max = np.array([2., 4.])
        assert_allclose(yure.calc_pos(), np.array([4/2, -2/4]))


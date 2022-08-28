from shippo_con import gui


class TestGUI:

    def test_is_local_version_outdated(self):
        assert     gui._is_local_version_outdated('1.10.0',  '1.9.0') # noqa
        assert not gui._is_local_version_outdated( '1.0.0',  '1.0.0') # noqa
        assert not gui._is_local_version_outdated( '1.0.9', '1.0.10') # noqa

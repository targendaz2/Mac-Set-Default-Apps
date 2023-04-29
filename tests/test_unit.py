import pytest

from msda import errors
from msda.main import _get_app_url, _get_role_utis

class TestUnit:

    def test_can_find_app_url_from_app_id_if_installed(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app_url = _get_app_url(app_id)

        # Then the app's URL should be returned
        assert app_url == '/Applications/Safari.app'

    def test_cant_find_app_url_from_app_id_if_not_installed(self):
        # Given the ID of an app that isn't installed
        app_id = 'com.dgrdev.fakebrowser'

        # When that app ID is submitted
        # Then an appropriate error should be raised
        with pytest.raises(errors.AppNotFoundError):
            _get_app_url(app_id)

    def test_can_load_appropriate_config_for_a_known_app_role(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        _get_role_utis(app_role)

        # The corresponding role file should be loaded
        from msda.main import app_role_file
        assert 'browser.yml' in app_role_file

    def test_cant_load_config_for_an_unknown_app_role(self):
        # Given the name of an unknown app role
        app_role = 'scuba'

        # When that app role is submitted
        # Then an appropriate error should be raised
        with pytest.raises(errors.UnknownRoleError):
            _get_role_utis(app_role)

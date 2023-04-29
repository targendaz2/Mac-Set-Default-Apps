import pytest

from msda import models

class TestAppLookups:

    def test_can_find_app_url_from_app_id_if_installed(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the app's URL should be returned
        assert app.url == '/Applications/Safari.app'

    def test_cant_find_app_url_from_app_id_if_not_installed(self):
        # Given the ID of an app that isn't installed
        app_id = 'com.dgrdev.fakebrowser'

        # When that app ID is submitted
        # Then an appropriate error should be raised
        with pytest.raises(models.App.AppNotFoundError):
            models.App(id=app_id)

class TestAppRoleLoading:

    def test_cant_find_config_for_an_unknown_app_role(self):
        # Given the name of an unknown app role
        app_role = 'scuba'

        # When that app role is submitted
        # Then an appropriate error should be raised
        with pytest.raises(models.Role.UnknownRoleError):
            models.Role(name=app_role)

    def test_loads_specified_app_role_if_it_exists(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # The corresponding role file should be loaded
        from msda.main import app_role_settings
        assert 'protocols' in role.settings
        assert 'utis' in role.settings

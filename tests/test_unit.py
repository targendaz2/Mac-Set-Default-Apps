import pytest

from UniformTypeIdentifiers import UTType, UTTypeHTML, UTTypeURL

from msda import models

class TestAppModel:

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

class TestRoleModel:

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

    def test_loads_appropriate_UTTypes_from_identifiers(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # The appropriate UTTypes should be loaded
        uttype_xhtml = UTType.typeWithIdentifier_('public.xhtml')

        assert UTTypeHTML in role._utis
        assert UTTypeURL in role._utis
        assert uttype_xhtml in role._utis

    def test_loads_appropriate_protocols_from_role_definition(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # The appropriate UTTypes should be loaded

        assert 'http' in role._protocols
        assert 'https' in role._protocols

import pytest

from Cocoa import NSWorkspace
from UniformTypeIdentifiers import UTType, UTTypeHTML, UTTypeURL

from msda import models

class TestAppModel:

    def test_can_find_app_url_from_app_id_if_installed(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the app's URL should be returned
        assert app.url == NSWorkspace.new().URLForApplicationWithBundleIdentifier_(app_id)

    def test_cant_find_app_from_app_id_if_not_installed(self):
        # Given the ID of an app that isn't installed
        app_id = 'com.dgrdev.fakebrowser'

        # When that app ID is submitted
        # Then an appropriate error should be raised
        with pytest.raises(models.App.AppNotFoundError):
            models.App(id=app_id)

    def test_loads_supported_protocols(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the app's supported protocols should be available
        for protocol in ('http', 'https'):
            assert protocol in app.protocols

    def test_loads_supported_utis(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the UTTypes should be loaded
        uttype_xhtml = UTType.typeWithIdentifier_('public.xhtml')

        uttypes = (
            (UTTypeHTML, 'Viewer'),
            (UTTypeURL, 'Viewer'),
            (uttype_xhtml, 'Viewer'),
        )

        for uttype_set in uttypes:
            assert uttype_set in app.utis

    def test_supports_method_returns_true_for_supported_role(self):
        # Given an App object
        app = models.App(id='com.apple.Safari')

        # And a Role object that app should support
        role = models.Role(name='browser')

        # When the app is asked to check if it supports the role
        result = app.supports(role)

        # Then the function should return true
        assert result == True

class TestRoleModel:

    def test_cant_find_config_for_an_unknown_app_role(self):
        # Given the name of an unknown app role
        app_role = 'scuba'

        # When that app role is submitted
        # Then an appropriate error should be raised
        with pytest.raises(models.Role.UnknownRoleError):
            models.Role(name=app_role)

    def test_loads_appropriate_UTTypes_from_known_role(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # Then the appropriate UTTypes should be loaded
        uttype_xhtml = UTType.typeWithIdentifier_('public.xhtml')

        for uttype in (UTTypeHTML, UTTypeURL, uttype_xhtml):
            assert uttype in role.utis

    def test_loads_appropriate_protocols_from_known_role(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # The appropriate protocols should set
        for protocol in ('http', 'https'):
            assert protocol in role.protocols

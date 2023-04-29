import pytest

from Cocoa import NSURL
from UniformTypeIdentifiers import UTType, UTTypeHTML, UTTypeURL

from msda import models

class TestAppModel:

    def test_can_find_app_url_from_app_id_if_installed(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the app's URL should be returned
        assert app.url == NSURL.fileURLWithPath_isDirectory_('/Applications/Safari.app', True)

    def test_cant_find_app_url_from_app_id_if_not_installed(self):
        # Given the ID of an app that isn't installed
        app_id = 'com.dgrdev.fakebrowser'

        # When that app ID is submitted
        # Then an appropriate error should be raised
        with pytest.raises(models.App.AppNotFoundError):
            models.App(id=app_id)

    @pytest.mark.skip(reason="Changing model to handle NSURLs")
    def test_loads_supported_protocols(self):
        # Given the ID of an installed app
        app_id = 'com.apple.Safari'

        # When that app ID is submitted
        app = models.App(id=app_id)

        # Then the app's supported protocols should be available
        assert 'html' in app._protocols

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

        # The appropriate UTTypes should be loaded
        uttype_xhtml = UTType.typeWithIdentifier_('public.xhtml')

        for uttype in (UTTypeHTML, UTTypeURL, uttype_xhtml):
            assert uttype in role._utis

    def test_loads_appropriate_protocols_from_known_role(self):
        # Given the name of an app role
        app_role = 'browser'

        # When that app role is submitted
        role = models.Role(name=app_role)

        # The appropriate protocols should set
        for protocol in ('http', 'https'):
            assert protocol in role._protocols

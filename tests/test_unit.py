from msda.main import _get_app_url

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
        app_url = _get_app_url(app_id)

        # Then nothing should be returned
        assert app_url == None

from msda.main import _get_app_url

class TestUnit:

    def test_can_find_app_url_from_app_name(self):
        # Given the name of an installed app
        app_name = 'Google Chrome'

        # When that app name is submitted
        app_url = _get_app_url(app_name)

        # Then the app's URL should be returned
        assert app_url == '/Applications/Google Chrome.app'

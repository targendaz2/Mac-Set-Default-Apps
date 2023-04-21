import subprocess
import webbrowser

from typer.testing import CliRunner

from msda.main import app

from .utils import is_running, not_running

runner = CliRunner()

class TestFunctional:

    def test_set_chrome_as_default_browser_for_current_user(self, monkeypatch):
        # Confirm initial OS state for testing purposes

        # Safari is not running
        assert not_running('Safari')

        # Google Chrome is not running
        assert not_running('Chrome')

        # Safari is the default browser
        # (we assume that if a URL is opened and Safari is then opened, Safari is the default browser)
        webbrowser.open('http://example.com')
        assert is_running('Safari')

        # Return to initial OS state to begin testing

        # Close Safari and confirm it closed
        command = 'pkill -l ^Safari$'.split()
        subprocess.run(command, capture_output=True)
        assert not_running('Safari')

        # Begin testing

        # User runs MSDA command to set Google Chrome as the default browser
        result = runner.invoke(app, ['set', 'Google Chrome.app', 'browser'])
        assert result.returncode == 0

        # Confirm resulting state

        # Google Chrome is the default browser
        # (we assume that if a URL is opened and Google Chrome is then opened, Google Chrome is the default browser)
        webbrowser.open('http://example.com')
        assert is_running('Chrome')

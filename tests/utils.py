import subprocess

def _app_state(app, running):
    command = f'pgrep -l ^{app}$'.split()
    result = subprocess.run(command, capture_output=True)

    expected_code = 0 if running == True else 1

    return result.returncode == expected_code

def is_running(app):
    return _app_state(app, running=True)

def not_running(app):
    return _app_state(app, running=False)

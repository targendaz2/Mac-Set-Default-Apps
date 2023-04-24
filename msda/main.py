import subprocess

# from Cocoa import NSWorkspace

import typer

# workspace = NSWorkspace.sharedWorkspace()
# setDefaultApplicationAtURL_toOpenContentType_completionHandler_
# setDefaultApplicationAtURL_toOpenContentTypeOfFileAtURL_completionHandler
# setDefaultApplicationAtURL_toOpenFileAtURL_completionHandler_
# setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler_

def callback():
    pass

app = typer.Typer(callback=callback)

def _get_app_url(app_id: str):
    command = f'mdfind kMDItemCFBundleIdentifier = {app_id}'
    result = subprocess.run(command.split(), capture_output=True)
    app_path = result.stdout.decode().strip()
    return app_path or None

@app.command('set')
def set_command(app_id: str, role: str):
    pass

if __name__ == '__main__':
    app(prog_name='msda')

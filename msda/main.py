import os
import subprocess

import yaml

# from Cocoa import NSWorkspace
from UniformTypeIdentifiers import UTType, UTTypeURL

from pprint import pprint

import typer

from . import errors

# workspace = NSWorkspace.sharedWorkspace()
# setDefaultApplicationAtURL_toOpenContentType_completionHandler_
# setDefaultApplicationAtURL_toOpenContentTypeOfFileAtURL_completionHandler
# setDefaultApplicationAtURL_toOpenFileAtURL_completionHandler_
# setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler_

app_role_file = ''
app_role_settings = {}

def callback():
    pass

app = typer.Typer(callback=callback)

def _get_app_url(app_id: str):
    command = f'mdfind kMDItemCFBundleIdentifier = {app_id}'
    result = subprocess.run(command.split(), capture_output=True)
    app_path = result.stdout.decode().strip()
    if not app_path:
        raise errors.AppNotFoundError
    return app_path

def _get_app_role(role: str):
    global app_role_file
    global app_role_settings
    app_role_file = f'config/roles/{role}.yml'
    
    if not os.path.isfile(app_role_file):
        raise errors.UnknownRoleError

    with open(app_role_file, 'r') as file:
        app_role_settings = yaml.load(file, Loader=yaml.FullLoader)
    
    # UTType.typeWithIdentifier_('public.html')

@app.command('set')
def set_command(app_id: str, role: str):
    pass

if __name__ == '__main__':
    app(prog_name='msda')

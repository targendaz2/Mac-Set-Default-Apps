from Cocoa import NSWorkspace

import typer

from pprint import pprint

workspace = NSWorkspace.sharedWorkspace()
# setDefaultApplicationAtURL_toOpenContentType_completionHandler_
# setDefaultApplicationAtURL_toOpenContentTypeOfFileAtURL_completionHandler
# setDefaultApplicationAtURL_toOpenFileAtURL_completionHandler_
# setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler_

def callback():
    pass

app = typer.Typer(callback=callback)

def _get_app_url(app_name: str):
    return f'/Applications/{app_name}.app'

@app.command('set')
def set_command(application: str, role: str):
    pass

if __name__ == '__main__':
    app(prog_name='msda')

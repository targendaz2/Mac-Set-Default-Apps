import typer

# from Cocoa import NSWorkspace

# workspace = NSWorkspace.sharedWorkspace()
# setDefaultApplicationAtURL_toOpenContentType_completionHandler_
# setDefaultApplicationAtURL_toOpenContentTypeOfFileAtURL_completionHandler
# setDefaultApplicationAtURL_toOpenFileAtURL_completionHandler_
# setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler_

app_role_settings = {}

def callback():
    pass

app = typer.Typer(callback=callback)

@app.command('set')
def set_command(app_id: str, role: str):
    pass

if __name__ == '__main__':
    app(prog_name='msda')

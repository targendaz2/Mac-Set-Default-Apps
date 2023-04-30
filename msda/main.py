import typer

from . import models

from Cocoa import NSWorkspace

def callback():
    pass

app = typer.Typer(callback=callback)

@app.command('set')
def set_command(app_id: str, role: str):
    target_app = models.App(id=app_id)
    target_role = models.Role(name=role)

    # workspace = NSWorkspace.new()
    # for protocol in target_role.protocols:
    #     workspace.setDefaultApplicationAtURL_toOpenURLsWithScheme_completionHandler_(target_app.url, protocol[0], None)

    # for uti in target_role.utis:
    #     workspace.setDefaultApplicationAtURL_toOpenContentType_completionHandler_(target_app.url, uti, None)



if __name__ == '__main__':
    app(prog_name='msda')

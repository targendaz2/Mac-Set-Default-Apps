import typer

def callback():
    pass

app = typer.Typer(callback=callback)

@app.command('set')
def set_command(application: str, role: str):
    pass

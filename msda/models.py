from dataclasses import dataclass, field
import subprocess

from . import errors

@dataclass
class App:
    id: str
    url: str = field(init=False)
    
    def __post_init__(self):
        command = f'mdfind kMDItemCFBundleIdentifier = {self.id}'
        result = subprocess.run(command.split(), capture_output=True)
        self.url = result.stdout.decode().strip()
        if not self.url:
            raise errors.AppNotFoundError

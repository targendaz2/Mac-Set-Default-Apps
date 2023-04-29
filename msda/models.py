from dataclasses import dataclass, field
import os
import subprocess

import yaml

# from UniformTypeIdentifiers import UTType, UTTypeURL

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

@dataclass
class Role:
    name: str
    file: str = field(init=False)
    settings: dict = field(init=False)

    def __post_init__(self):
        # UTType.typeWithIdentifier_('public.html')
        self.file = f'config/roles/{self.name}.yml'
        if not os.path.isfile(self.file):
            raise errors.UnknownRoleError

        with open(self.file, 'r') as file:
            self.settings = yaml.load(file, Loader=yaml.FullLoader)

from dataclasses import dataclass, field
import os
import subprocess

import yaml

from UniformTypeIdentifiers import UTType

@dataclass
class App:
    id: str
    url: str = field(init=False)

    class AppNotFoundError(Exception):
        pass
    
    def __post_init__(self):
        command = f'mdfind kMDItemCFBundleIdentifier = {self.id}'
        result = subprocess.run(command.split(), capture_output=True)
        self.url = result.stdout.decode().strip()
        if not self.url:
            raise self.AppNotFoundError

@dataclass
class Role:
    name: str
    file: str = field(init=False)
    settings: dict = field(init=False)
    _utis: list = field(init=False, default_factory=list)

    class UnknownRoleError(Exception):
        pass


    def __post_init__(self):
        self.file = f'config/roles/{self.name}.yml'
        if not os.path.isfile(self.file):
            raise self.UnknownRoleError

        with open(self.file, 'r') as file:
            self.settings = yaml.load(file, Loader=yaml.FullLoader)

        for uti in self.settings['utis'].keys():
            self._utis.append(UTType.typeWithIdentifier_(uti))

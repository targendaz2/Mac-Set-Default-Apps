from dataclasses import dataclass, field
import os
import subprocess

import yaml

from pprint import pprint

from Cocoa import NSURL
from Foundation import NSBundle
from UniformTypeIdentifiers import UTType

@dataclass
class App:
    id: str
    url: NSURL = field(init=False)
    _bundle: NSBundle = field(init=False)
    _protocols: list = field(init=False)

    class AppNotFoundError(Exception):
        pass

    def _get_url(self):
        # Get app URL from identifier
        command = f'mdfind kMDItemCFBundleIdentifier = {self.id}'
        result = subprocess.run(command.split(), capture_output=True)
        url = result.stdout.decode().strip()
        if not url:
            raise self.AppNotFoundError
        self.url = NSURL.fileURLWithPath_isDirectory_(url, True)

    def _get_bundle(self):
        # Get app bundle from URL
        if not hasattr(self, 'url'):
            self._get_url()

        self._bundle = NSBundle.bundleWithURL_(self.url)

    def _get_protocols(self):
        # Parse supported protocols from bundle
        bundle_url_types = self._bundle.objectForInfoDictionaryKey_(
            'CFBundleURLTypes')
        self._protocols = [
            scheme for item in bundle_url_types for scheme in item['CFBundleURLSchemes']]
    
    def __post_init__(self):
        self._get_bundle()
        self._get_protocols()

@dataclass
class Role:
    name: str
    file: str = field(init=False)
    _protocols: list[str] = field(init=False, default_factory=list)
    _utis: list[UTType] = field(init=False, default_factory=list)

    class UnknownRoleError(Exception):
        pass

    def __post_init__(self):
        self.file = f'config/roles/{self.name}.yml'
        if not os.path.isfile(self.file):
            raise self.UnknownRoleError

        with open(self.file, 'r') as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)

        self._protocols = settings['protocols']

        self._utis = [UTType.typeWithIdentifier_(
            uti) for uti in settings['utis'].keys()]

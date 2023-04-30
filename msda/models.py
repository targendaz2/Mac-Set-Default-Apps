from dataclasses import dataclass, field
import os

import yaml

from pprint import pprint

from Cocoa import NSBundle, NSURL, NSWorkspace
from UniformTypeIdentifiers import UTType, UTTypeURL


@dataclass
class Role:
    name: str
    file: str = field(init=False)
    protocols: list[str] = field(init=False, default_factory=list)
    utis: list[UTType] = field(init=False, default_factory=list)

    class UnknownRoleError(Exception):
        pass

    def __post_init__(self):
        self.file = f'config/roles/{self.name}.yml'
        if not os.path.isfile(self.file):
            raise self.UnknownRoleError

        with open(self.file, 'r') as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)

        self.protocols = settings.get('protocols', [])

        for uti, role in settings.get('utis', {}).items():
            uttype = UTType.typeWithIdentifier_(uti)
            self.utis.append((uttype, role))

@dataclass
class App:
    id: str
    url: NSURL = field(init=False)
    protocols: list[str] = field(init=False, default_factory=list)
    utis: list = field(init=False, default_factory=list)
    _bundle: NSBundle = field(init=False)

    class AppNotFoundError(Exception):
        pass

    def _get_url(self):
        # Get app URL from identifier
        self.url = NSWorkspace.new().URLForApplicationWithBundleIdentifier_(self.id)
        if not self.url:
            raise self.AppNotFoundError

    def _get_bundle(self):
        # Get app bundle from URL
        if not hasattr(self, 'url'):
            self._get_url()

        self._bundle = NSBundle.bundleWithURL_(self.url)

    def _get_utis(self):
        doc_types = self._bundle.objectForInfoDictionaryKey_(
            'CFBundleDocumentTypes')

        for item in doc_types:
            if 'LSItemContentTypes' in item.keys():
                uttype = UTType.typeWithIdentifier_(
                    item['LSItemContentTypes'][0])
            elif 'CFBundleTypeMIMETypes' in item.keys():
                uttype = UTType.typeWithMIMEType_(
                    item['CFBundleTypeMIMETypes'][0])
            elif 'CFBundleTypeExtensions' in item.keys():
                extension = item['CFBundleTypeExtensions'][0]
                if extension == 'url':
                    uttype = UTTypeURL
                else:
                    uttype = UTType.typeWithFilenameExtension_(
                    extension)

            self.utis.append((uttype, item['CFBundleTypeRole']))

    def _get_protocols(self):
        # Parse supported protocols from bundle
        bundle_url_types = self._bundle.objectForInfoDictionaryKey_(
            'CFBundleURLTypes')
        self.protocols = [scheme for item in bundle_url_types for scheme in item['CFBundleURLSchemes']]
    
    def __post_init__(self):
        self._get_bundle()
        self._get_utis()
        self._get_protocols()

    def supports(self, role: Role):
        return True

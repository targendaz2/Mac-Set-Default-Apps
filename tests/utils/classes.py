import os
import shutil
import sys
import tempfile
from unittest import TestCase

from .factories import *
from .settings import *

module_path = os.path.abspath(os.path.join(THIS_FILE, '../payload'))
if module_path not in sys.path:
    sys.path.append(module_path)

import msda


# Abstract Classes
class LaunchServicesTestCase(TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix=msda.TMP_PREFIX)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def seed_plist(self, plist_name, location=None, target_name=None):
        if location == None:
            location = self.tmp

        if target_name == None:
            target_name = plist_name

        src = os.path.join(THIS_FILE, 'assets', plist_name)
        dest = os.path.join(location, target_name)

        parent_path = os.path.dirname(dest)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path)

        shutil.copy(src, dest)
        return dest

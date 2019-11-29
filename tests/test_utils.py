import imp, os
import shutil
import tempfile
from unittest import TestCase

from factories import *
from test_settings import *

msda = imp.load_source('msda', os.path.join(
    THIS_FILE, '../payload/msda.py')
)


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

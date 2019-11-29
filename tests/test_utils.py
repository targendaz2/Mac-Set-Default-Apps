import imp, os
import shutil
import tempfile
from unittest import TestCase

import factory

from fake.lshandler_properties import *
from test_settings import *

msda = imp.load_source('msda', os.path.join(
    THIS_FILE, '../payload/msda.py')
)

# Factories
def create_user_homes(num, location):
    created_user_homes = []
    for n in range(num):
        user_home_path = os.path.join(location, fake.user_name())
        os.makedirs(user_home_path)
        created_user_homes.append(user_home_path)

    return created_user_homes


class LSHandlerFactory(factory.Factory):

    class Meta:
        model = msda.LSHandler

    class Params:
        use_all = True
        extension_only = False
        protocol_only = False
        uti_only = False

    app_id = fake_app_id()

    @factory.lazy_attribute
    def uti(self):
        rand_num = random()
        if self.extension_only:
            return msda.EXTENSION_UTI
        elif self.protocol_only:
            return fake_protocol()
        elif self.uti_only:
            return fake_uti()
        elif rand_num < 0.1:
            return msda.EXTENSION_UTI
        elif rand_num <= 0.55:
            return fake_protocol()
        elif rand_num > 0.55:
            return fake_uti()

    @factory.lazy_attribute
    def role(self):
        if '.' in self.uti:
            return fake_role(all=self.use_all)
        return None

    @factory.lazy_attribute
    def extension(self):
        if self.uti == msda.EXTENSION_UTI:
            return fake_extension()
        return None

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

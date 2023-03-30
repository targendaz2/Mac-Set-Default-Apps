import os
import sys

import factory

from fake.lshandler_properties import *
from .settings import *

module_path = os.path.abspath(os.path.join(__file__, '../../../payload'))
if module_path not in sys.path:
    sys.path.append(module_path)

import msda


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

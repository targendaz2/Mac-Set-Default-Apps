import imp, os
from random import choice, random
import shutil
import tempfile
from unittest import TestCase

import factory
from faker import Faker
from faker.providers import file, internet, lorem

from test_settings import *

msda = imp.load_source('msda', os.path.join(
    THIS_FILE, '../payload/msda')
)

fake = Faker()
fake.add_provider(file)
fake.add_provider(internet)
fake.add_provider(lorem)

# Faker Functions
def fake_app_id():
    app_id = '{}.{}.{}'.format(
        fake.tld(),
        fake.domain_word(),
        fake.word(),
    )
    if random() > 0.1:
        return app_id 					# 90% chance: com.company.app
    return app_id + '.' + fake.word()	# 10% chance: com.company.app.pro

def fake_uti():
    if random() > 0.25:
        return 'public.{}'.format(		# 75% chance: public.html
            fake.file_extension()
        )
    uti = '{}.{}.{}'.format(
        fake.tld(),
        fake.domain_word(),
        fake.file_extension(),
    )
    if random() > 0.8:
        return uti						# 20% chance: com.company.file
    return '{}.{}.{}.{}'.format(		#  5% chance: com.company.app.file
        fake.tld(),
        fake.domain_word(),
        fake.word(),
        fake.file_extension(),
    )

def fake_protocol():
    protocols = [
        'http',
        'https',
        'xml',
        'xhtml',
        'ftp',
    ]
    return choice(protocols)

def fake_role(all=False):
    roles = ['editor', 'viewer']
    if all:
        roles.append('all')
    return choice(roles)

# Sample LSHandlers
html_viewer_lshandler = msda.LSHandler(
    app_id=fake_app_id(),
    uti=fake_uti(),
    role=fake_role(),
)

https_lshandler = msda.LSHandler(
    app_id=fake_app_id(),
    uti=fake_protocol(),
)

url_all_lshandler = msda.LSHandler(
    app_id=fake_app_id(),
    uti=fake_uti(),
)


# Sample LSHandler Dicts
def protocol_lshandler_dict(app_id, uti):
    role_key = 'LSHandlerRoleAll'
    dict_ = {
        'LSHandlerURLScheme': uti.lower(),
        role_key: app_id,
        'LSHandlerPreferredVersions': {
            role_key: '-',
        }
    }
    return dict_

def uti_lshandler_dict(app_id, uti, role='all'):
    role_key = 'LSHandlerRole' + role.capitalize()
    dict_ = {
        'LSHandlerContentType': uti,
        role_key: app_id,
        'LSHandlerPreferredVersions': {
            role_key: '-',
        }
    }
    return dict_

# LSHandler Factories
class LSHandlerFactory(factory.Factory):

    class Meta:
        model = msda.LSHandler

    class Params:
        rand_num = random()
        use_all = True
        use_uti = False
        use_protocol = False

    app_id = fake_app_id()

    @factory.lazy_attribute
    def uti(self):
        if (self.rand_num > 0.5 and not self.use_uti) or self.use_uti:
            return fake_uti()
        if (self.rand_num <= 0.5 and not self.use_protocol) or self.use_protocol:
            return fake_protocol()

    @factory.lazy_attribute
    def role(self):
        if (self.rand_num > 0.5 and not self.use_uti) or self.use_uti:
            return fake_role(all=self.use_all)


def lshandler_factory(num=1, all=True, uti=False, protocol=False):
    return LSHandlerFactory.build_batch(num,
        app_id=fake_app_id(),
        use_all=all,
        use_uti=uti,
        use_protocol=protocol,
    )

# Abstract Classes
class LaunchServicesTestCase(TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix=msda.TMP_PREFIX)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def seed_plist(self, plist_name):
        src = os.path.join(THIS_FILE, 'assets', plist_name)
        dest = os.path.join(self.tmp, plist_name)
        shutil.copy(src, dest)
        return dest

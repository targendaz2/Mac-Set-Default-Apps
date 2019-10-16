import imp, os
from random import choice, random

from faker import Faker
from faker.providers import file, internet, lorem

from test_settings import THIS_FILE

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda')
)

fake = Faker()
fake.add_provider(file)
fake.add_provider(internet)
fake.add_provider(lorem)

# Sample LSHandlers
html_viewer_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='public.html',
	role='viewer'
)

https_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='https',
)

url_all_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='public.url',
)

# Functions
def fake_app_id():
	app_id = '{}.{}.{}'.format(
		fake.tld(),
		fake.domain_word(),
		fake.word(),
	)
	if random() > 0.1:
		return app_id
	return app_id + '.' + fake.word()

def fake_uti():
	if random() > 0.1:
		return 'public.' + fake.file_extension()
	uti = '{}.{}.{}'.format(
		fake.tld(),
		fake.domain_word(),
		fake.file_extension(),
	)
	return uti

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

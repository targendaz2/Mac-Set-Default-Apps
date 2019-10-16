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

# LSHandler Factories
def lshandler_factory(num=1, all=True, uti=False, protocol=False):
	app_id = fake_app_id()
	handlers = []
	utis = []
	for n in range(num):
		rand_num = random()
		if rand_num > 0.5 or uti:
			uti = fake_uti()
			role = fake_role(all=all)
			handler = msda.LSHandler(
				app_id=app_id,
				uti=uti,
				role=role
			)
		elif rand_num <= 0.5 or protocol:
			uti = fake_protocol()
			handler = msda.LSHandler(
				app_id=app_id,
				uti=uti,
			)
		handlers.append(handler)
	return handlers

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

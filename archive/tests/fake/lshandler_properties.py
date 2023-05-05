from random import choice, random

from faker import Faker
from faker.providers import file, internet, lorem

fake = Faker()
fake.add_provider(file)
fake.add_provider(internet)
fake.add_provider(lorem)


def fake_app_id():
    app_id = '{}.{}.{}'.format(
        fake.tld(),
        fake.domain_word(),
        fake.word(),
    )
    if random() > 0.1:
        return app_id 					# 90% chance: com.company.app
    return app_id + '.' + fake.word()	# 10% chance: com.company.app.pro

def fake_extension():
    return str(fake.file_extension())

def fake_protocol():
    protocols = [
        'http',
        'https',
        'xml',
        'xhtml',
        'ftp',
    ]
    return choice(protocols)

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

def fake_role(all=False):
    roles = ['editor', 'viewer']
    if all:
        roles.append('all')
    return choice(roles)

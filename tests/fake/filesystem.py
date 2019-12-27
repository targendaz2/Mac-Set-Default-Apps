from __future__ import print_function

import imp
import os
import tempfile

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)

FAKE_FS_ROOT = tempfile.mkdtemp()
USER_HOMES_DIR = 'Users'

def create_user_homes(number=1):
	created_user_homes = []
	for n in range(number):
		user_home_path = os.path.join(
			FAKE_FS_ROOT,
			USER_HOMES_DIR,
			fake.user_name(),
		)
		os.makedirs(user_home_path)
		created_user_homes.append(user_home_path)
	return created_user_homes

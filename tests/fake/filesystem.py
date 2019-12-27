from __future__ import print_function

import imp
import os
import shutil
import tempfile

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)

TMP_PREFIX = 'fake_fs_'
USER_HOMES_DIR_NAME = 'Users'

BASE_DIRS = (
	os.path.join(USER_HOMES_DIR_NAME, '.localized'),
	os.path.join(USER_HOMES_DIR_NAME, 'Shared', '.localized'),
)

class FakeFileSystem(object):

	def create_base_fs(self):
		for path in BASE_DIRS:
			os.makedirs(os.path.join(
				self.ROOT_DIR,
				path,
			))

	def __init__(self):
		self.ROOT_DIR = tempfile.mkdtemp(prefix=TMP_PREFIX)
		self.create_base_fs()

	def __del__(self):
		shutil.rmtree(self.ROOT_DIR)

	@property
	def USER_HOMES_DIR(self):
		return os.path.join(
			self.ROOT_DIR,
			USER_HOMES_DIR_NAME,
		)

	def create_user_homes(self, number=1):
		created_user_homes = []
		for n in range(number):
			user_home_path = os.path.join(
				self.USER_HOMES_DIR,
				fake.user_name(),
			)
			os.makedirs(user_home_path)
			created_user_homes.append(user_home_path)
		return created_user_homes

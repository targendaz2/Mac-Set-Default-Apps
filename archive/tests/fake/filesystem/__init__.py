from __future__ import print_function

import imp
import os as real_os
import shutil
import tempfile
from unittest import TestCase

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)

TMP_PREFIX = 'fake_fs_'
USER_HOMES_DIR_NAME = 'Users'
USER_TEMPLATE_PATH = real_os.path.join(
	'Library',
	'User Template',
	'English.lproj',
)

BASE_PATHS = [
	real_os.path.join(USER_HOMES_DIR_NAME, '.localized'),
	real_os.path.join(USER_HOMES_DIR_NAME, 'Shared', '.localized'),
]

BASE_USER_PATHS = (
	real_os.path.join('Library', 'Preferences', 'com.apple.launchservices'),
)

for path in BASE_USER_PATHS:
	BASE_PATHS.append(real_os.path.join(
		USER_TEMPLATE_PATH, path,
	))

class MockOS(object):

	def __getattr__(self, attr):
		print('mock os call')
		return getattr(real_os, attr)

class FakeFSTestCase(TestCase):

	def create_base_fs(self, paths, root=None):
		if not root:
			root = self.ROOT_DIR

		for path in paths:
			real_os.makedirs(real_os.path.join(
				root,
				path,
			))

	def setUp(self):
		self.ROOT_DIR = tempfile.mkdtemp(prefix=TMP_PREFIX)
		self.create_base_fs(BASE_PATHS)

	def tearDown(self):
		shutil.rmtree(self.ROOT_DIR)

	@property
	def USER_HOMES_DIR(self):
		return real_os.path.join(
			self.ROOT_DIR,
			USER_HOMES_DIR_NAME,
		)

	def create_user_homes(self, number=1):
		created_user_homes = []
		for n in range(number):
			user_home_path = real_os.path.join(
				self.USER_HOMES_DIR,
				fake.user_name(),
			)
			self.create_base_fs(BASE_USER_PATHS, root=user_home_path)
			created_user_homes.append(user_home_path)
		return created_user_homes

#!/usr/bin/env python3

from __future__ import print_function

import unittest
from unittest import TestCase

import os
import sys
from random import randint

import mock

from fake.filesystem import (
	BASE_PATHS, BASE_USER_PATHS, FakeFSTestCase, USER_HOMES_DIR_NAME,
	USER_TEMPLATE_PATH, MockOS
)
from utils.settings import *

module_path = os.path.abspath(os.path.join(THIS_FILE, '../payload'))
if module_path not in sys.path:
    sys.path.append(module_path)

import msda

class TestFakeFileSystemFunctions(FakeFSTestCase):

	def test_all_base_folders_are_created(self):
		for path in BASE_PATHS:
			self.assertTrue(os.path.exists(os.path.join(
				self.ROOT_DIR,
				path,
			)))

	def test_creates_English_user_template_by_default(self):
		self.assertTrue(os.path.exists(os.path.join(
			self.ROOT_DIR,
			USER_TEMPLATE_PATH,
		)))

	def test_base_user_folders_are_created_in_English_user_template(self):
		for path in BASE_USER_PATHS:
			self.assertTrue(os.path.exists(os.path.join(
				self.ROOT_DIR,
				USER_TEMPLATE_PATH,
				path,
			)))

	def test_can_create_single_user_home(self):
		user_homes = self.create_user_homes(1)
		self.assertTrue(os.path.exists(user_homes[0]))

	def test_can_create_multiple_user_homes(self):
		num_homes = randint(2, 10)
		user_homes = self.create_user_homes(num_homes)
		self.assertEqual(num_homes, len(user_homes))
		for user_home in user_homes:
			self.assertTrue(os.path.exists(user_home))

	def test_user_homes_dont_persist_between_tests(self):
		self.assertEqual(
			os.listdir(self.USER_HOMES_DIR),
			['.localized', 'Shared'],
		)

	def test_created_user_homes_have_base_structure(self):
		user_homes = self.create_user_homes(randint(1, 10))
		for user_home in user_homes:
			for path in BASE_USER_PATHS:
				self.assertTrue(os.path.exists(os.path.join(
					user_home, path
				)))

class TestMockOSFunctions(TestCase):

	def test_pass_through(self):
		print(MockOS().path.exists('/'))


if __name__ == '__main__':
    unittest.main()

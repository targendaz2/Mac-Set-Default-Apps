#!/usr/bin/env python3

from __future__ import print_function

import unittest

import os
import sys
from random import randint, random

import mock

from utils.classes import *
from utils.settings import *

module_path = os.path.abspath(os.path.join(THIS_FILE, '../payload'))
if module_path not in sys.path:
    sys.path.append(module_path)

import msda


class FunctionalTests(LaunchServicesTestCase):

	def setUp(self):
		super(FunctionalTests, self).setUp()
		self.user_ls_path = self.seed_plist(SIMPLE_BINARY_PLIST)
		self.user_ls = msda.LaunchServices(self.user_ls_path)
		self.template_ls_path = os.path.join(
			self.tmp, 'com.apple.LaunchServices.Secure.plist'
		)
		self.template_ls = msda.LaunchServices(self.template_ls_path)

	@mock.patch('msda.create_user_ls_path')
	def test_set_single_uti_handler_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handler = LSHandlerFactory(uti_only=True)

		self.assertNotIn(handler, self.user_ls.handlers)

		arguments = [
			'set',
			handler.app_id,
			'-u', handler.uti, handler.role,
		]
		msda.main(arguments)

		self.user_ls.read()
		self.assertIn(handler, self.user_ls.handlers)

	@mock.patch('msda.create_user_ls_path')
	def test_set_single_protocol_handler_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handler = LSHandlerFactory(protocol_only=True)

		self.assertNotIn(handler, self.user_ls.handlers)

		arguments = [
			'set',
			handler.app_id,
			'-p', handler.uti,
		]
		msda.main(arguments)

		self.user_ls.read()
		self.assertIn(handler, self.user_ls.handlers)

	@mock.patch('msda.create_user_ls_path')
	def test_set_multiple_uti_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = LSHandlerFactory.build_batch(randint(3, 6), uti_only=True)

		arguments = ['set', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)

			arguments.extend(['-u', handler.uti, handler.role,])
		msda.main(arguments)

		self.user_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)

	@mock.patch('msda.create_user_ls_path')
	def test_set_multiple_protocol_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = LSHandlerFactory.build_batch(randint(3, 6), protocol_only=True)

		arguments = ['set', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)

			arguments.extend(['-p', handler.uti])
		msda.main(arguments)

		self.user_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)

	@mock.patch('msda.create_user_ls_path')
	def test_set_multiple_mixed_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = LSHandlerFactory.build_batch(randint(3, 6))

		arguments = ['set', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)

			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])
		msda.main(arguments)

		self.user_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)

	@mock.patch('msda.create_user_ls_path')
	@mock.patch('msda.create_template_ls_path')
	def test_set_handlers_for_current_user_and_template(self, template_fn, user_fn):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = LSHandlerFactory.build_batch(randint(4, 6))

		arguments = ['set', '-fut', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])
		msda.main(arguments)

		self.user_ls.read()
		self.template_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)
			self.assertIn(handler, self.template_ls.handlers)
			self.assertIn(handler.app_id, self.template_ls.app_ids)

	@mock.patch('msda.create_user_ls_path')
	@mock.patch('msda.create_template_ls_path')
	@mock.patch('msda.get_current_username', return_value='')
	def test_set_handlers_for_only_template(self,
		get_current_username, template_fn, user_fn,
	):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = LSHandlerFactory.build_batch(randint(4, 6))

		arguments = ['set', '-fut', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])
		msda.main(arguments)

		self.user_ls.read()
		self.template_ls.read()
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertIn(handler, self.template_ls.handlers)
			self.assertIn(handler.app_id, self.template_ls.app_ids)

	@mock.patch('msda.create_user_ls_path')
	@mock.patch('msda.create_template_ls_path')
	@mock.patch('msda.JAMF', True)
	def test_set_handlers_for_current_user_and_template_in_Jamf(self,
		template_fn, user_fn,
	):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = LSHandlerFactory.build_batch(randint(1, 3))

		arguments = ['', '', '', 'set -fut ' + handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments[3] += ' -e ' + handler.extension + ' ' + handler.role
				else:
					arguments[3] += ' -u ' + handler.uti + ' ' + handler.role
			else:
				arguments[3] += ' -p ' + handler.uti
		msda.main(arguments)

		self.user_ls.read()
		self.template_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)
			self.assertIn(handler, self.template_ls.handlers)
			self.assertIn(handler.app_id, self.template_ls.app_ids)

	def test_set_handlers_for_all_existing_users(self,):
		fake_user_home_location = os.path.join(self.tmp, 'Users')
		fake_user_homes = create_user_homes(randint(1, 3), fake_user_home_location)
		handlers = LSHandlerFactory.build_batch(randint(4, 6))
		arguments = ['set', '-feu', handlers[0].app_id]

		for handler in handlers:
			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])

		for user_home in fake_user_homes:
			user_ls_path = self.seed_plist(
				SIMPLE_BINARY_PLIST,
				os.path.join(user_home, msda.PLIST_RELATIVE_LOCATION),
				msda.PLIST_NAME,
			)
			user_ls = msda.LaunchServices(user_ls_path)
			for handler in handlers:
				self.assertNotIn(handler, user_ls.handlers)
				self.assertNotIn(handler.app_id, user_ls.app_ids)

		with mock.patch('msda.USER_HOMES_LOCATION', fake_user_home_location):
			msda.main(arguments)

		for user_home in fake_user_homes:
			user_ls.read()
			for handler in handlers:
				self.assertIn(handler, user_ls.handlers)
				self.assertIn(handler.app_id, user_ls.app_ids)

	@mock.patch('msda.create_template_ls_path')
	def test_set_handlers_for_all_existing_users_and_user_template(self,
		template_fn
	):
		template_fn.return_value = self.template_ls_path
		fake_user_home_location = os.path.join(self.tmp, 'Users')
		fake_user_homes = create_user_homes(randint(1, 3), fake_user_home_location)
		handlers = LSHandlerFactory.build_batch(randint(4, 6))
		arguments = ['set', '-feu', '-fut', handlers[0].app_id]

		for handler in handlers:
			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])

		for user_home in fake_user_homes:
			user_ls_path = self.seed_plist(
				SIMPLE_BINARY_PLIST,
				os.path.join(user_home, msda.PLIST_RELATIVE_LOCATION),
				msda.PLIST_NAME,
			)
			user_ls = msda.LaunchServices(user_ls_path)
			for handler in handlers:
				self.assertNotIn(handler, user_ls.handlers)
				self.assertNotIn(handler.app_id, user_ls.app_ids)

		with mock.patch('msda.USER_HOMES_LOCATION', fake_user_home_location):
			msda.main(arguments)

		for user_home in fake_user_homes:
			user_ls.read()
			for handler in handlers:
				self.assertIn(handler, user_ls.handlers)
				self.assertIn(handler.app_id, user_ls.app_ids)

	def test_set_handlers_for_all_existing_valid_users(self,):
		fake_user_home_location = os.path.join(self.tmp, 'Users')
		fake_user_homes = create_user_homes(randint(3, 5), fake_user_home_location)
		num_invalid_users = randint(1, 2)
		handlers = LSHandlerFactory.build_batch(randint(4, 6))
		arguments = ['set', '-feu', handlers[0].app_id]

		for handler in handlers:
			if '.' in handler.uti:
				if handler.uti == msda.EXTENSION_UTI:
					arguments.extend(['-e', handler.extension, handler.role])
				else:
					arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])

		for user_home in fake_user_homes[:-num_invalid_users]:
			user_ls_path = os.path.join(
				user_home,
				msda.PLIST_RELATIVE_LOCATION,
				msda.PLIST_NAME,
			)
			os.makedirs(os.path.dirname(user_ls_path))
			user_ls = msda.LaunchServices(user_ls_path)
			for handler in handlers:
				self.assertNotIn(handler, user_ls.handlers)
				self.assertNotIn(handler.app_id, user_ls.app_ids)

		with mock.patch('msda.USER_HOMES_LOCATION', fake_user_home_location):
			msda.main(arguments)

		for user_home in fake_user_homes[:-num_invalid_users]:
			user_ls.read()
			for handler in handlers:
				self.assertIn(handler, user_ls.handlers)
				self.assertIn(handler.app_id, user_ls.app_ids)

		for user_home in fake_user_homes[-num_invalid_users:]:
			self.assertFalse(os.path.exists(os.path.join(
				user_home,
				msda.PLIST_RELATIVE_LOCATION,
				msda.PLIST_NAME,
			)))

	@mock.patch('msda.create_user_ls_path')
	def test_set_single_extension_handler_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handler = LSHandlerFactory(extension_only=True)

		self.assertNotIn(handler, self.user_ls.handlers)

		arguments = [
			'set',
			handler.app_id,
			'-e', handler.extension, 'all',
		]
		msda.main(arguments)

		self.user_ls.read()
		self.assertIn(handler, self.user_ls.handlers)


if __name__ == '__main__':
    unittest.main()

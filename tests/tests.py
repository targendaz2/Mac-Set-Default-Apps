#!/usr/bin/env python

from __future__ import print_function

import unittest
from unittest import TestCase

import imp
import os
from plistlib import readPlist
from random import randint, random
import shutil
import sys
import tempfile

import mock

from test_settings import *
from test_utils import *

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda.py')
)

class TestLaunchServicesTestCaseSetUpAndTearDown(LaunchServicesTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setUp_creates_tmp_directory(self):
        super(TestLaunchServicesTestCaseSetUpAndTearDown, self).setUp()
        self.assertIsNotNone(self.tmp)
        self.assertTrue(os.path.exists(self.tmp))

    def test_tearDown_removes_tmp_directory(self):
        super(TestLaunchServicesTestCaseSetUpAndTearDown, self).setUp()
        super(TestLaunchServicesTestCaseSetUpAndTearDown, self).tearDown()
        self.assertFalse(os.path.exists(self.tmp))


class TestLaunchServicesTestCaseMethods(LaunchServicesTestCase):

    def test_seed_plist_copies_plist_into_tmp(self):
        self.assertTrue(os.path.exists(os.path.join(
            THIS_FILE, 'assets', SIMPLE_BINARY_PLIST,
        )))
        tmp_path = self.seed_plist(SIMPLE_BINARY_PLIST)
        self.assertTrue(os.path.exists(tmp_path))


class TestLSHandlerObject(TestCase):

	def test_can_generate_LSHandler_for_uti(self):
		sample_lshandler = LSHandlerFactory.build(uti_only=True)
		comparison_dict = uti_lshandler_dict(
			app_id=sample_lshandler.app_id,
			uti=sample_lshandler.uti,
			role=sample_lshandler.role,
		)
		self.assertEqual(dict(sample_lshandler), comparison_dict)

	def test_lshandlers_for_utis_have_role_default_to_all(self):
		sample_lshandler = LSHandlerFactory.build(uti_only=True, role=None)
		comparison_dict = uti_lshandler_dict(
			app_id=sample_lshandler.app_id,
			uti=sample_lshandler.uti,
			role='all',
		)
		self.assertEqual(dict(sample_lshandler), comparison_dict)

	def test_can_generate_LSHandler_for_protocol(self):
		sample_lshandler = LSHandlerFactory.build(protocol_only=True)
		comparison_dict = protocol_lshandler_dict(
			app_id=sample_lshandler.app_id,
			uti=sample_lshandler.uti,
		)
		self.assertEqual(dict(sample_lshandler), comparison_dict)


class TestLSHandlerObjectEquality(TestCase):

	html_all = msda.LSHandler(
		app_id='org.company2.fakebrowser',
		uti='public.html',
		role='all',
	)

	html_viewer1 = msda.LSHandler(
		app_id='com.company1.fakebrowser',
		uti='public.html',
		role='viewer',
	)

	html_viewer2 = msda.LSHandler(
		app_id='org.company2.fakebrowser',
		uti='public.html',
		role='viewer',
	)

	html_reader = msda.LSHandler(
		app_id='com.company.fakebrowser',
		uti='public.html',
		role='reader',
	)

	mailto_protocol = msda.LSHandler(
		app_id='com.company.fakebrowser',
		uti='mailto',
	)

	def test_equal_if_same_uti_and_role(self):
		uti = fake_uti()
		role = fake_role(all=False)
		self.assertEqual(
			LSHandlerFactory(uti=uti, role=role),
			LSHandlerFactory(uti=uti, role=role),
		)

	def test_not_equal_if_different_uti(self):
		self.assertNotEqual(self.html_viewer1, self.mailto_protocol)

	def test_not_equal_if_different_role_but_neither_is_all(self):
		self.assertNotEqual(self.html_viewer1, self.html_reader)

	def test_equal_if_same_uti_and_existing_role_is_all(self):
		self.assertEqual(self.html_viewer1, self.html_all)

	def test_equal_if_same_uti_and_replacing_role_is_all(self):
		self.assertEqual(self.html_all, self.html_viewer1)


class TestLaunchServicesObject(LaunchServicesTestCase):

	def setUp(self):
		super(TestLaunchServicesObject, self).setUp()
		self.ls = msda.LaunchServices()
		self.ls2 = msda.LaunchServices()

	def test_can_read_binary_plists(self):
		self.ls.plist = self.seed_plist(SIMPLE_BINARY_PLIST)

		self.ls.read()
		self.assertEqual(dict(self.ls), EMPTY_LS_PLIST)

	def test_returns_base_plist_if_non_existant(self):
		self.ls.plist = os.path.join(self.tmp, SIMPLE_BINARY_PLIST)
		self.assertFalse(os.path.isfile(self.ls.plist))

		self.ls.read()
		self.assertEqual(dict(self.ls), EMPTY_LS_PLIST)

	def test_can_write_binary_plists(self):
		self.ls.plist = self.seed_plist(XML_PLIST)
		dest_plist = os.path.join(self.tmp, 'tmp.secure.plist')
		self.ls.read()
		self.ls.write(dest_plist)

		self.ls2.plist = dest_plist
		self.ls2.read()
		self.assertEqual(dict(self.ls), dict(self.ls2))

	def test_can_write_binary_plists_if_directory_structure_doesnt_exist(self):
		self.ls.plist = self.seed_plist(XML_PLIST)
		dest_plist = os.path.join(self.tmp, 'new.dir/tmp.secure.plist')
		self.ls.read()
		self.ls.write(dest_plist)

		self.ls2.plist = dest_plist
		self.ls2.read()
		self.assertEqual(dict(self.ls), dict(self.ls2))

	def test_stores_LSHandlers_in_contained_list(self):
		src_plist = self.seed_plist(BINARY_PLIST)
		self.ls.plist = src_plist
		self.ls.read()
		self.assertIsInstance(self.ls.handlers[0], msda.LSHandler)

	def test_populates_self_if_provided_plist(self):
		ls = msda.LaunchServices(self.seed_plist(BINARY_PLIST))
		self.assertIsInstance(ls.handlers[0], msda.LSHandler)

	def test_can_set_handlers(self):
		ls = msda.LaunchServices(self.seed_plist(SIMPLE_BINARY_PLIST))
		ls.set_handler(
			app_id='edu.school.browser',
			uti='public.html',
			role='viewer',
		)
		expected_handler = msda.LSHandler(
			app_id='edu.school.browser',
			uti='public.html',
			role='viewer',
		)

		self.assertEqual(dict(ls.handlers[0]), dict(expected_handler))

	def test_can_check_for_set_app_IDs(self):
		ls = msda.LaunchServices(self.seed_plist(SIMPLE_BINARY_PLIST))
		ls.set_handler(
			app_id='edu.school.browser',
			uti='public.html',
			role='viewer',
		)
		ls.set_handler(
			app_id='edu.school.email',
			uti='mailto',
		)

		self.assertIn('edu.school.browser', ls.app_ids)
		self.assertIn('edu.school.email', ls.app_ids)

	def test_overwrites_single_handler_for_same_uti_and_role(self):
		ls = msda.LaunchServices(self.seed_plist(SIMPLE_BINARY_PLIST))
		old_handler = ls.set_handler(
			app_id='edu.school.browser',
			uti='public.html',
			role='viewer',
		)

		self.assertIn(old_handler.app_id, ls.app_ids)

		new_handler = ls.set_handler(
			app_id='org.bigorg.browser',
			uti='public.html',
			role='viewer',
		)

		self.assertNotIn(old_handler.app_id, ls.app_ids)
		self.assertIn(new_handler.app_id, ls.app_ids)

	def test_overwrites_all_handlers_for_same_uti_and_role(self):
		ls = msda.LaunchServices(self.seed_plist(SIMPLE_BINARY_PLIST))
		old_handlers = [
			ls.set_handler(
				app_id='edu.school.browser',
				uti='public.html',
				role='viewer',
			),
			ls.set_handler(
				app_id='edu.school.browser',
				uti='public.html',
				role='reader',
			),
			ls.set_handler(
				app_id='edu.school.browser',
				uti='public.html',
				role='writer',
			),
		]

		for old_handler in old_handlers:
			self.assertIn(old_handler.app_id, ls.app_ids)

		new_handler = ls.set_handler(
			app_id='org.bigorg.browser',
			uti='public.html',
			role='all',
		)

		for old_handler in old_handlers:
			self.assertNotIn(old_handler.app_id, ls.app_ids)
		self.assertIn(new_handler.app_id, ls.app_ids)

	def test_can_set_LSHandler_from_object(self):
		ls = msda.LaunchServices(self.seed_plist(SIMPLE_BINARY_PLIST))
		handler = lshandler_factory(all=True)

		self.assertNotIn(handler, ls.handlers)
		ls.set_handler(handler)
		self.assertIn(handler, ls.handlers)


@mock.patch('msda.create_user_ls_path')
class FunctionalTests(LaunchServicesTestCase):

	def setUp(self):
		super(FunctionalTests, self).setUp()
		self.user_ls_path = self.seed_plist(SIMPLE_BINARY_PLIST)
		self.user_ls = msda.LaunchServices(self.user_ls_path)
		self.template_ls_path = os.path.join(
			self.tmp, 'com.apple.LaunchServices.Secure.plist'
		)
		self.template_ls = msda.LaunchServices(self.template_ls_path)

	def test_set_single_uti_handler_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handler = lshandler_factory(uti=True)[0]

		self.assertNotIn(handler, self.user_ls.handlers)

		arguments = [
			'set',
			handler.app_id,
			'-u', handler.uti, handler.role,
		]
		msda.main(arguments)

		self.user_ls.read()
		self.assertIn(handler, self.user_ls.handlers)

	def test_set_single_protocol_handler_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handler = lshandler_factory(protocol=True)[0]

		self.assertNotIn(handler, self.user_ls.handlers)

		arguments = [
			'set',
			handler.app_id,
			'-p', handler.uti,
		]
		msda.main(arguments)

		self.user_ls.read()
		self.assertIn(handler, self.user_ls.handlers)

	def test_set_multiple_uti_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = lshandler_factory(uti=True, num=randint(3, 6))

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

	def test_set_multiple_protocol_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = lshandler_factory(protocol=True, num=randint(3, 6))

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

	def test_set_multiple_protocol_and_uti_handlers_for_current_user(self, user_fn):
		user_fn.return_value = self.user_ls_path
		handlers = lshandler_factory(num=randint(3, 6))

		arguments = ['set', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)

			if '.' in handler.uti:
				arguments.extend(['-u', handler.uti, handler.role])
			else:
				arguments.extend(['-p', handler.uti])
		msda.main(arguments)

		self.user_ls.read()
		for handler in handlers:
			self.assertIn(handler, self.user_ls.handlers)
			self.assertIn(handler.app_id, self.user_ls.app_ids)

	@mock.patch('msda.create_template_ls_path')
	def test_set_handlers_for_current_user_and_template(self, template_fn, user_fn):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = lshandler_factory(num=randint(4, 6))

		arguments = ['set', '-fut', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
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

	@mock.patch('msda.create_template_ls_path')
	@mock.patch('msda.get_current_username', return_value='')
	def test_set_handlers_for_only_template(self,
		get_current_username, template_fn, user_fn,
	):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = lshandler_factory(num=randint(4, 6))

		arguments = ['set', '-fut', handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
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

	@mock.patch('msda.create_template_ls_path')
	@mock.patch('msda.JAMF', True)
	def test_set_handlers_for_current_user_and_template_in_Jamf(self,
		template_fn, user_fn,
	):
		user_fn.return_value = self.user_ls_path
		template_fn.return_value = self.template_ls_path
		handlers = lshandler_factory(num=randint(1, 3))

		arguments = ['', '', '', 'set -fut ' + handlers[0].app_id]
		for handler in handlers:
			self.assertNotIn(handler, self.user_ls.handlers)
			self.assertNotIn(handler.app_id, self.user_ls.app_ids)
			self.assertNotIn(handler, self.template_ls.handlers)
			self.assertNotIn(handler.app_id, self.template_ls.app_ids)

			if '.' in handler.uti:
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


if __name__ == '__main__':
    unittest.main()

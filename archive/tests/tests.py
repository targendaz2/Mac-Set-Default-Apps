#!/usr/bin/env python3

from __future__ import print_function

import unittest
from unittest import TestCase

import os
from random import randint, random
import shutil
import sys
import tempfile

import mock

from utils.classes import *
from utils.settings import *

module_path = os.path.abspath(os.path.join(THIS_FILE, '../payload'))
if module_path not in sys.path:
    sys.path.append(module_path)

import msda


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


class TestFunctions(LaunchServicesTestCase):

	def test_gather_user_ls_paths(self):
		fake_user_homes = create_user_homes(3, self.tmp)
		for fake_user_home in fake_user_homes:
			self.seed_plist(
				SIMPLE_BINARY_PLIST,
				os.path.join(fake_user_home, msda.PLIST_RELATIVE_LOCATION),
				msda.PLIST_NAME,
			)

		with mock.patch('msda.USER_HOMES_LOCATION', self.tmp):
			gathered_ls_paths = msda.gather_user_ls_paths()

		for fake_user_home in fake_user_homes:
			fake_ls_path = os.path.join(
				fake_user_home,
				msda.PLIST_RELATIVE_LOCATION,
				msda.PLIST_NAME
			)
			self.assertIn(fake_ls_path, gathered_ls_paths)


class TestLSHandlerObject(TestCase):

	def test_LSHandler_can_be_converted_to_dict(self):
		sample_lshandler = LSHandlerFactory()
		self.assertIsInstance(dict(sample_lshandler), dict)

	def test_can_generate_LSHandler_for_uti(self):
		sample_lshandler = LSHandlerFactory(uti_only=True)
		sample_dict = dict(sample_lshandler)
		self.assertIn(sample_lshandler.app_id, sample_dict.values())
		self.assertIn(sample_lshandler.uti, sample_dict.values())
		self.assertIn(
			'LSHandlerRole' + sample_lshandler.role.capitalize(),
			sample_dict.keys()
		)

	def test_can_generate_LSHandler_for_protocol(self):
		sample_lshandler = LSHandlerFactory(protocol_only=True)
		sample_dict = dict(sample_lshandler)
		self.assertIn(sample_lshandler.app_id, sample_dict.values())
		self.assertIn(sample_lshandler.uti, sample_dict.values())
		self.assertIn('LSHandlerRoleAll', sample_dict.keys())

	def test_can_generate_LSHandler_for_extension(self):
		sample_lshandler = LSHandlerFactory(extension_only=True)
		self.assertEqual(sample_lshandler.uti, msda.EXTENSION_UTI)

		sample_dict = dict(sample_lshandler)
		self.assertIn(sample_lshandler.app_id, sample_dict.values())
		self.assertIn(sample_lshandler.uti, sample_dict.values())
		self.assertIn(
			'LSHandlerRole' + sample_lshandler.role.capitalize(),
			sample_dict.keys()
		)
		self.assertIn('LSHandlerContentTag', sample_dict.keys())
		self.assertIn(sample_lshandler.extension, sample_dict.values())


class TestLSHandlerObjectEquality(TestCase):

	def test_equal_if_same_uti_and_role(self):
		uti = fake_uti()
		role = fake_role(all=False)
		self.assertEqual(
			LSHandlerFactory(uti=uti, role=role),
			LSHandlerFactory(uti=uti, role=role),
		)

	def test_not_equal_if_different_uti(self):
		self.assertNotEqual(
			LSHandlerFactory(uti='public.html'),
			LSHandlerFactory(uti='mailto'),
		)

	def test_not_equal_if_different_role_but_neither_is_all(self):
		uti = fake_uti()
		self.assertNotEqual(
			LSHandlerFactory(uti=uti, role='viewer'),
			LSHandlerFactory(uti=uti, role='editor'),
		)

	def test_equal_if_same_uti_and_existing_role_is_all(self):
		uti = fake_uti()
		self.assertEqual(
			LSHandlerFactory(uti=uti, role='all'),
			LSHandlerFactory(uti=uti, use_all=False),
		)

	def test_equal_if_same_uti_and_replacing_role_is_all(self):
		uti = fake_uti()
		self.assertEqual(
			LSHandlerFactory(uti=uti, use_all=False),
			LSHandlerFactory(uti=uti, role='all'),
		)

	def test_not_equal_if_different_extension(self):
		uti = msda.EXTENSION_UTI
		self.assertNotEqual(
			LSHandlerFactory(uti=uti, extension='pdf'),
			LSHandlerFactory(uti=uti, extension='cr'),
		)

	def test_not_equal_if_same_extension_and_different_not_all_role(self):
		uti = msda.EXTENSION_UTI
		extension = fake_extension()
		self.assertNotEqual(
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='viewer',
			),
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='editor',
			),
		)

	def test_not_equal_if_same_extension_and_existing_role_is_all(self):
		uti = msda.EXTENSION_UTI
		extension = fake_extension()
		self.assertEqual(
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='all',
			),
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='editor',
			),
		)

	def test_not_equal_if_same_extension_and_replacing_role_is_all(self):
		uti = msda.EXTENSION_UTI
		extension = fake_extension()
		self.assertEqual(
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='viewer',
			),
			LSHandlerFactory(
				uti=uti,
				extension=extension,
				role='all',
			),
		)


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
		handler = LSHandlerFactory(use_all=True)

		self.assertNotIn(handler, ls.handlers)
		ls.set_handler(handler)
		self.assertIn(handler, ls.handlers)

if __name__ == '__main__':
    unittest.main()

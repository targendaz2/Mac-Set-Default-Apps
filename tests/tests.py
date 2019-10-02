#!/usr/bin/python

import imp
import os
from plistlib import readPlist
import shutil
import sys
import tempfile
import unittest

from test_settings import *

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda')
)


class TestLaunchServicesObject(unittest.TestCase):

	def setUp(self):
		self.tmp = tempfile.mkdtemp(prefix=TMP_PREFIX)
		self.launchservices = msda.LaunchServices()

	def tearDown(self):
		shutil.rmtree(self.tmp)

	def seed_plist(self, plist_name):
		src = os.path.join(THIS_FILE, 'assets', plist_name)
		dest = os.path.join(self.tmp, plist_name)
		shutil.copy(src, dest)
		return dest

	def test_can_read_binary_plists(self):
		binary_plist = self.seed_plist(SIMPLE_BINARY_PLIST)

		self.launchservices.read(binary_plist)
		self.assertEqual(dict(self.launchservices), EMPTY_LS_PLIST)

	def test_returns_base_plist_if_non_existant(self):
		nonexistant_plist = os.path.join(self.tmp, SIMPLE_BINARY_PLIST)
		self.assertFalse(os.path.isfile(nonexistant_plist))

		self.launchservices.read(nonexistant_plist)
		self.assertEqual(dict(self.launchservices), EMPTY_LS_PLIST)

	def test_can_write_binary_plists(self):
		src_plist = self.seed_plist(XML_PLIST)
		dest_plist = os.path.join(self.tmp, 'tmp.secure.plist')
		xml_contents = readPlist(src_plist)

		self.launchservices.write(xml_contents, dest_plist)
		self.launchservices.read(dest_plist)
		self.assertEqual(xml_contents, dict(self.launchservices))

	def test_can_write_binary_plists_if_directory_structure_doesnt_exist(self):
		src_plist = self.seed_plist(XML_PLIST)
		dest_plist = os.path.join(self.tmp, 'new.dir/tmp.secure.plist')
		xml_contents = readPlist(src_plist)

		self.launchservices.write(xml_contents, dest_plist)
		self.launchservices.read(dest_plist)
		self.assertEqual(xml_contents, dict(self.launchservices))


class TestLSHandlerObject(unittest.TestCase):

	def test_can_generate_LSHandler_for_uti(self):
		app_id = 'com.company.fakebrowser'
		uti = 'public.html'
		role = 'viewer'

		lshandler = msda.LSHandler(
			app_id=app_id,
			uti=uti,
			role=role,
		)

		role_key = 'LSHandlerRole' + role.capitalize()
		comparison_dict = {
			'LSHandlerContentType': uti,
			role_key: app_id,
			'LSHandlerPreferredVersions': {
				role_key: '-',
			}
		}
		self.assertEqual(dict(lshandler), comparison_dict)

	def test_lshandlers_for_utis_have_role_default_to_all(self):
		app_id = 'com.company.fakebrowser'
		uti = 'public.url'

		lshandler = msda.LSHandler(
			app_id=app_id,
			uti=uti,
		)

		comparison_dict = {
			'LSHandlerContentType': uti,
			'LSHandlerRoleAll': app_id,
			'LSHandlerPreferredVersions': {
				'LSHandlerRoleAll': '-',
			}
		}
		self.assertEqual(dict(lshandler), comparison_dict)

	def test_can_generate_LSHandler_for_protocol(self):
		app_id = 'com.company.fakebrowser'
		protocol = 'https'

		lshandler = msda.LSHandler(
			app_id=app_id,
			uti=protocol,
		)

		role_key = 'LSHandlerRoleAll'
		comparison_dict = {
			'LSHandlerURLScheme': protocol.lower(),
			role_key: app_id,
			'LSHandlerPreferredVersions': {
				role_key: '-',
			}
		}
		self.assertEqual(dict(lshandler), comparison_dict)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python

import imp
import os
from plistlib import readPlist
import shutil
import sys
import tempfile
import unittest

from test_settings import *
from test_utils import *

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda')
)


class TestLaunchServicesObject(unittest.TestCase):

	def setUp(self):
		self.tmp = tempfile.mkdtemp(prefix=TMP_PREFIX)
		self.launchservices = msda.LaunchServices()

	def tearDown(self):
		shutil.rmtree(self.tmp)

	def test_can_read_binary_plists(self):
		tmp_plist = seed_simple_binary_plist(self.tmp)

		self.launchservices.read(tmp_plist)
		self.assertEqual(dict(self.launchservices), EMPTY_LS_PLIST)

	def test_returns_base_plist_if_non_existant(self):
		tmp_plist = os.path.join(self.tmp, SIMPLE_BINARY_PLIST_NAME)
		self.assertFalse(os.path.isfile(tmp_plist))

		self.launchservices.read(tmp_plist)
		self.assertEqual(dict(self.launchservices), EMPTY_LS_PLIST)

	def test_can_write_binary_plists(self):
		tmp_xml_plist = seed_xml_plist(self.tmp)
		tmp_binary_plist = os.path.join(self.tmp, 'tmp.secure.plist')
		xml_contents = readPlist(tmp_xml_plist)

		self.launchservices.write(xml_contents, tmp_binary_plist)
		self.launchservices.read(tmp_binary_plist)
		self.assertEqual(xml_contents, dict(self.launchservices))

	def test_can_write_binary_plists_if_directory_structure_doesnt_exist(self):
		tmp_xml_plist = seed_xml_plist(self.tmp)
		tmp_binary_plist = os.path.join(self.tmp, 'new.dir/tmp.secure.plist')
		xml_contents = readPlist(tmp_xml_plist)

		self.launchservices.write(xml_contents, tmp_binary_plist)
		self.launchservices.read(tmp_binary_plist)
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

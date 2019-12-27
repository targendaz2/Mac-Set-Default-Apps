#!/usr/bin/env python

from __future__ import print_function

import unittest
from unittest import TestCase

import imp
import os
from random import randint

import mock

from fake import filesystem as fs
from utils.settings import *

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda.py')
)


class TestFakeFileSystemFunctions(TestCase):

	def test_can_create_single_user_home(self):
		user_homes = fs.create_user_homes(1)
		self.assertTrue(os.path.exists(user_homes[0]))

	def test_can_create_multiple_user_homes(self):
		num_homes = randint(2, 10)
		user_homes = fs.create_user_homes(num_homes)
		self.assertEqual(num_homes, len(user_homes))
		for user_home in user_homes:
			self.assertTrue(os.path.exists(user_home))


if __name__ == '__main__':
    unittest.main()

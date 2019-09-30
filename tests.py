#!/usr/bin/python

import imp
import unittest

msda = imp.load_source('msda', 'payload/msda')

class TestBasicFunctions(unittest.TestCase):

	def test_can_identify_standard_UTIs(self):
		test_string = 'com.company.fakeapp'
		result = msda.is_uti(test_string)
		self.assertTrue(result)

	def test_can_identify_longer_UTIs(self):
		test_string = 'com.company.fakeapp.pro'
		result = msda.is_uti(test_string)
		self.assertTrue(result)

	def test_can_identify_non_UTIs(self):
		test_string = 'http'
		result = msda.is_uti(test_string)
		self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

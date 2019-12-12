#!/usr/bin/env python

from __future__ import print_function

import unittest
from unittest import TestCase

import imp

import mock

from fake import filesystem as fs
from utils.settings import *

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda.py')
)


class TestFakeFileSystemFunctions(TestCase):

	pass


if __name__ == '__main__':
    unittest.main()

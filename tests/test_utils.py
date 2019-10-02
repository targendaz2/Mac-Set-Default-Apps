import os, shutil

from test_settings import *

def seed_simple_binary_plist(tmp_dir):
	plist = os.path.join(tmp_dir, SIMPLE_BINARY_PLIST_NAME)
	shutil.copy(SIMPLE_BINARY_PLIST, plist)
	return plist

def seed_xml_plist(tmp_dir):
	plist = os.path.join(tmp_dir, XML_PLIST_NAME)
	shutil.copy(XML_PLIST, plist)
	return plist

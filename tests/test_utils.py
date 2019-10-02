import os, shutil

from test_settings import *

def seed_plist(plist_name, plist, tmp_dir):
	seeded_plist = os.path.join(tmp_dir, plist_name)
	shutil.copy(plist, seeded_plist)
	return seeded_plist

def seed_simple_binary_plist(tmp_dir):
	return seed_plist(SIMPLE_BINARY_PLIST_NAME, SIMPLE_BINARY_PLIST, tmp_dir)

def seed_xml_plist(tmp_dir):
	return seed_plist(XML_PLIST_NAME, XML_PLIST, tmp_dir)

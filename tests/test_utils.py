import os, shutil

from test_settings import *

def seed_plist(plist_name, tmp_dir):
	src = os.path.join(THIS_FILE, 'assets', plist_name)
	dest = os.path.join(tmp_dir, plist_name)
	shutil.copy(src, dest)
	return dest

def seed_binary_plist(tmp_dir):
	return seed_plist(SIMPLE_BINARY_PLIST, tmp_dir)

def seed_xml_plist(tmp_dir):
	return seed_plist(XML_PLIST, tmp_dir)

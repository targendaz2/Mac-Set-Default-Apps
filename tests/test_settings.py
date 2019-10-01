import os, sys

THIS_FILE = os.path.dirname(sys.argv[0])

TMP_PREFIX = 'msda_tmp_'
SIMPLE_BINARY_PLIST_NAME = 'ex_simple_binary.plist'
SIMPLE_BINARY_PLIST = os.path.join(
	THIS_FILE, 'assets', SIMPLE_BINARY_PLIST_NAME
)
XML_PLIST_NAME = 'ex_xml.plist'
XML_PLIST = os.path.join(THIS_FILE, 'assets', XML_PLIST_NAME)

import os, sys

THIS_FILE = os.path.dirname(sys.argv[0])

TMP_ROOT = os.path.join(THIS_FILE, '..', 'tmp')
SIMPLE_BINARY_PLIST = 'ex_simple_binary.plist'
BINARY_PLIST = 'ex_binary.plist'
XML_PLIST = 'ex_xml.plist'
EMPTY_LS_PLIST = { 'LSHandlers': [] }

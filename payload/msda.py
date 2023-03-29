#!/usr/bin/python3

"""\
Directly modifies launchservices plists to set default file associations in macOS.

A somewhat complete list of UTI's can be found here:
    https://escapetech.eu/manuals/qdrop/uti.html\
"""

from __future__ import print_function

import os, shutil, subprocess, sys, time
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from platform import mac_ver
import plistlib
from tempfile import NamedTemporaryFile


###############################################################################
#
# User-Editable Settings
#
###############################################################################

JAMF = False                   # Is this being used as a Jamf script?
TMP_PREFIX = 'msda_tmp_'       # Prefixes tempoaray files created by this app
USER_HOMES_LOCATION = '/Users' # Where users' home directories are located


###############################################################################
#
# App Information
#
###############################################################################

__author__ = 'David G. Rosenberg'
__copyright__ = 'Copyright (c), Mac Set Default Apps'
__license__ = 'MIT'
__version__ = '1.3.1'
__email__ = 'dgrosenberg@icloud.com'


###############################################################################
#
# Settings Users Shouldn't Change
#
###############################################################################

EXTENSION_UTI = 'public.filename-extension'
LSREGISTER_BINARY = '/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister'
OS_VERSION = float(mac_ver()[0][3:])
PLIST_NAME = 'com.apple.launchservices.secure.plist'
PLIST_RELATIVE_LOCATION = 'Library/Preferences/com.apple.LaunchServices/'
USER_TEMPLATE_LOCATION = '/Library/User Template/English.lproj'

if OS_VERSION < 15.0:
    USER_TEMPLATE_LOCATION = os.path.join(
        '/System', USER_TEMPLATE_LOCATION
    )


###############################################################################
#
# Functions
#
###############################################################################

def create_plist_parents(plist_path):
    """
    Creates the directory structure if the provided plist doesn't exist
    """

    # if the specified plist already exists, don't do anything
    if os.path.isfile(plist_path):
        return False

    # if the specified plist's parent directories already exist, don't do
    # anything
    parent_path = os.path.dirname(plist_path)
    if os.path.exists(parent_path):
        return False

    # create the parent directories for the specified plist
    os.makedirs(parent_path)
    return plist_path

def create_user_ls_path(username):
    path = os.path.join(
        USER_HOMES_LOCATION,
        username,
        PLIST_RELATIVE_LOCATION,
        PLIST_NAME,
    )
    return path

def create_template_ls_path():
    path = os.path.join(
        USER_TEMPLATE_LOCATION,
        PLIST_RELATIVE_LOCATION,
        PLIST_NAME,
    )
    return path

def get_current_username():
    with subprocess.Popen(("who"), stdout=subprocess.PIPE) as who_cmd:
        with subprocess.Popen(
            ("grep", "console"), stdin=who_cmd.stdout, stdout=subprocess.PIPE
        ) as grep_cmd:
            with subprocess.Popen(
                ("cut", "-d", " ", "-f1"), stdin=grep_cmd.stdout, stdout=subprocess.PIPE
            ) as username_cmd:
                return subprocess.check_output(
                    ("head", "-n", "1"), stdin=username_cmd.stdout
                ).strip().decode("utf-8")

def gather_user_ls_paths():
    gathered_users = os.listdir(USER_HOMES_LOCATION)
    ls_paths = []
    for user in gathered_users:
        user_ls_path = create_user_ls_path(user)
        if os.path.exists(os.path.dirname(user_ls_path)):
            ls_paths.append(user_ls_path)

    return ls_paths


###############################################################################
#
# Class Definitions
#
###############################################################################

class LSHandler(object):

    def _from_dict(self, from_dict):
        """
        Creates an LSHandler object from a dictionary
        """

        # preset extension
        self.extension = None

        # grab the role from the string containing it
        self.role = list(from_dict['LSHandlerPreferredVersions'].keys())[0]
        self.role = self.role[13:].lower()

        # grab the UTI/protocol/extension
        try:
            # for if it's a UTI
            self.uti = from_dict['LSHandlerContentType'].lower()
            self._type = 'ContentType'
        except KeyError:
            pass
        try:
            # for if it's an extension
            self.uti = from_dict['LSHandlerContentTagClass'].lower()
            self._type = 'ContentTagClass'
            self.extension = from_dict['LSHandlerContentTag'].lower()
        except KeyError:
            pass
        try:
            # for if it's a protocol
            self.uti = from_dict['LSHandlerURLScheme'].lower()
            self._type = 'URLScheme'
        except KeyError:
            pass

        # grab the App ID
        self.app_id = from_dict[self._role_key].lower()

    def _from_properties(self, **kwargs):
        """
        Creates an LSHandler from specified properties
        """
        self.app_id = kwargs['app_id'].lower()
        self.uti = kwargs['uti'].lower()
        self.extension = None

        # determines if we're working with a UTI or protocol based on the
        # presence of periods
        if '.' in self.uti:
            self.role = kwargs.get('role') or 'all'
            self.role = self.role.lower()
            self._type = 'ContentType'

            # additionally determine if we're working with a file extension
            if self.uti == EXTENSION_UTI:
                self.extension = kwargs['extension'].lower()
                self._type = 'ContentTagClass'
        else:
            self._type = 'URLScheme'
            self.role = 'all'

    def __init__(self, from_dict=None, **kwargs):
        if from_dict:
            self._from_dict(from_dict)
        else:
            self._from_properties(**kwargs)

    @property
    def _role_key(self):
        """
        Generates the dictionary key for an LSHandler's role
        """
        return 'LSHandlerRole' + self.role.capitalize()

    def __eq__(self, other):
        """
        Two LSHandlers for the same role and UTI would be considered equal
        """
        compare_utis = self.uti == other.uti
        compare_extensions = self.extension == other.extension
        if self.role == 'all' or other.role == 'all':
            compare_roles = True
        else:
            compare_roles = self.role == other.role
        return compare_utis and compare_roles and compare_extensions

    def __ne__(self, other):
        """
        Inverts the __eq__ function
        """
        return not self == other

    def __iter__(self):
        yield ('LSHandler' + self._type, self.uti)
        yield (self._role_key, self.app_id)
        yield ('LSHandlerPreferredVersions', { self._role_key: '-' })
        if self.extension:
            yield('LSHandlerContentTag', self.extension)


class LaunchServices(object):

    def __init__(self, plist=None):
        self.handlers = []
        self.plist = plist

        if self.plist:
            self.read()

    def __iter__(self):
        yield ('LSHandlers', [ dict(h) for h in self.handlers ])

    def read(self):
        """
        Reads the plist at the specified path into a LaunchServices object,
        creating LSHandler objects as necesary
        """

        # is the specified plist doesn't exist, there's nothing to read
        if not os.path.isfile(self.plist):
            return

        with NamedTemporaryFile(prefix=TMP_PREFIX, delete=True) as tmp_plist:
            # copy the target plist to a temporary file
            tmp_path = tmp_plist.name
            shutil.copyfile(self.plist, tmp_path)

            # convert to XML from binary
            convert_command = '/usr/bin/plutil -convert xml1 ' + tmp_path
            subprocess.check_output(convert_command.split())

            # read the plist
            with open(tmp_path, "rb") as file:
                plist = plistlib.load(file)

        # convert any specified LSHandlers to objects
        for lshandler in plist['LSHandlers']:
            self.handlers.append(LSHandler(from_dict=lshandler))

    def write(self, plist=None):
        """
        Writes this object to the specified plist, formatting it as a
        LaunchServices plist
        """

        # allow for alternate destinations (mostly for testing)
        if not plist:
            plist = self.plist

        # create parent directories if they don't exist
        create_plist_parents(plist)

        with NamedTemporaryFile(prefix=TMP_PREFIX, delete=True) as tmp_plist:
            # write the LaunchServices object to a temporary file
            tmp_path = tmp_plist.name
            with open(tmp_path, "wb") as file:
                plistlib.dump(dict(self), file)

            # convert it to binary
            convert_command = '/usr/bin/plutil -convert binary1 ' + tmp_path
            subprocess.check_output(convert_command.split())

            # and overwrite the specified plist
            shutil.copyfile(tmp_path, plist)

    @property
    def app_ids(self):
        """
        Provides a set of all App IDs set as default handlers
        """
        collected_app_ids = [ h.app_id for h in self.handlers ]
        return set(collected_app_ids)

    def set_handler(self, lshandler=None, **kwargs):
        """
        Adds the provided LSHandler to the LaunchServices object, converting
        to a new LSHandler if necesary
        """
        if not lshandler:
            new_lshandler = LSHandler(**kwargs)
        else:
            new_lshandler = lshandler
        self.handlers = [ h for h in self.handlers if h != new_lshandler ]
        self.handlers.append(new_lshandler)
        return new_lshandler


###############################################################################
#
# Main Functions
#
###############################################################################

def set_command(args):
    # print('Setting "{}" as a default handler in...'.format(args.app_id))

    # Check for current user
    current_username = get_current_username()

    # Collect plists
    plists = []
    if args.feu:
        plists.extend(gather_user_ls_paths())
    elif current_username != '':
        plists.append(create_user_ls_path(current_username))
    if args.fut:
        plists.append(create_template_ls_path())

    # Process plists
    for plist in plists:
        ls = LaunchServices(plist)
        # print('  "{}"...'.format(ls.plist))

        # Combine submitted UTIs and protocols
        if not args.uti:
            args.uti = []
        if args.protocol:
            args.uti += [ [p, None] for p in args.protocol ]

        # Create and set UTI and protocol handlers
        for uti in args.uti:
            # if uti[1] != None:
            #   print('    for "{}" with role "{}"'.format(uti[0], uti[1]))
            # else:
            #   print('    for "{}" with role "all"'.format(uti[0]))
            ls.set_handler(
                app_id=args.app_id,
                uti=uti[0],
                role=uti[1],
            )

        # Create and set extension handlers
        if args.extension:
            for extension in args.extension:
                ls.set_handler(
                    app_id=args.app_id,
                    uti=EXTENSION_UTI,
                    role=extension[1],
                    extension=extension[0],
                )

        ls.write()
    return 0

def main(arguments=None):
    if JAMF:
        # Strip first 3 args and convert 4th to a list
        arguments = arguments[3].split()

    # Global parser setup
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
        epilog='Please email {} with any issues'.format(
            __email__,
        )
    )
    # parser.add_argument(
    #   '-v', '--verbose',
    #   help='verbose output',
    #   action='store_true',
    # )
    parser.add_argument(
        '--version',
        help='prints the current version',
        action='version',
        version=__version__,
    )
    subparsers = parser.add_subparsers(
        help='the subcommand to run',
        metavar='command',
        dest='command',
    )

    # "set" parser setup
    set_parser = subparsers.add_parser(
        'set',
        help='set LSHandlers for a given App ID',
    )
    set_parser.set_defaults(func=set_command)
    set_parser.add_argument(
        'app_id',
        help='the identifier of the application to set as a default',
        type=str,
    )
    set_parser.add_argument(
        '-feu',
        help='updates all existing users\' launch services',
        action='store_true',
    )
    set_parser.add_argument(
        '-fut',
        help='updates the user template\'s launch services',
        action='store_true',
    )
    set_parser.add_argument(
        '-e', '--extension',
        help='file extensions to associate with the given app ID',
        action='append',
        nargs=2,
        metavar=('EXTENSION', 'ROLE'),
    )
    set_parser.add_argument(
        '-p', '--protocol',
        help='protocols to associate with the given app ID',
        action='append',
    )
    set_parser.add_argument(
        '-u', '--uti',
        help='UTIs and roles to associate with the given app ID',
        action='append',
        nargs=2,
        metavar=('UTI', 'ROLE'),
    )

    # Process specified args
    args = parser.parse_args(arguments)
    # global verbose
    # verbose = args.verbose

    # print('')

    # Run specified function with processed args
    return args.func(args)


if __name__ == '__main__':
    # Determine whether to run as a user or as root
    username = get_current_username()
    if username in ['', 'root', '_mbsetupuser']:
        sudo_command = '/usr/bin/sudo -u root'
        domains = 'local,system'
    else:
        sudo_command = '/usr/bin/sudo -u ' + username
        domains = 'user,local,system'
    
    # Do the thing
    exit_code = main(sys.argv[1:])

    # Kill any running launchservice processes
    kill_command = '/usr/bin/killall lsd'
    subprocess.check_output(sudo_command.split() + kill_command.split())

    # Rebuild the launchservices database
    rebuild_command = [LSREGISTER_BINARY,
        '-kill', '-r', '-f',
        '-all', domains,
    ]
    subprocess.check_output(sudo_command.split() + rebuild_command)

    sys.exit(exit_code)

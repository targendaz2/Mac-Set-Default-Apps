#!/usr/bin/python

import os
import plistlib
import shutil
import subprocess
import sys


# Process submitted arguments
app_id = str(sys.argv[4])
settings = [ str(x).split(',') for x in sys.argv[5:] if x != '' ]

print ''
print 'Running with app ID for "{}"'.format(app_id)
print 'Running with settings {}'.format(settings)


# Functions
def get_current_username():
    from SystemConfiguration import SCDynamicStoreCopyConsoleUser
    username = (SCDynamicStoreCopyConsoleUser(None, None, None) or [None])[0]
    username = [username,""][username in [u"loginwindow", None, u""]]
    print 'Current username is "{}"'.format(username)
    return username

def read_binary_plist(plist_path):
    # Check if plist exists
    if not os.path.isfile(plist_path):
        # If not, check if its parents exist
        plist_parent_path = os.path.dirname(plist_path)
        if not os.path.exists(plist_parent_path):
            # If not, make them
            import errno
            try:
                os.makedirs(plist_parent_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        # Return an empty plist for comparison
        return { 'LSHandlers': [] }

    filename = os.path.basename(plist_path)
    tmp_path = os.path.join('/tmp', filename + '.tmp')

    shutil.copy(plist_path, tmp_path)

    convert_command = '/usr/bin/plutil -convert xml1 {}'.format(tmp_path)
    subprocess.check_output(convert_command.split())

    plist = plistlib.readPlist(tmp_path)
    os.remove(tmp_path)

    print 'Reading "{}"'.format(plist_path)
    return plist

def write_binary_plist(dict_, plist_path):
    filename = os.path.basename(plist_path)
    tmp_path = os.path.join('/tmp', filename + '.tmp')

    plistlib.writePlist(dict_, tmp_path)

    convert_command = '/usr/bin/plutil -convert binary1 {}'.format(tmp_path)
    subprocess.check_output(convert_command.split())

    shutil.copy(tmp_path, plist_path)
    os.remove(tmp_path)

    print 'Writing "{}"'.format(plist_path)
    return True

def gen_lshandler(app_id, uti, role):
    lshandler = {}

    if role.lower() != 'url':
        lshandler['LSHandlerContentType'] = uti
    else:
        lshandler['LSHandlerURLScheme'] = uti
        role = 'all'

    role_key = 'LSHandlerRole' + role.capitalize()

    lshandler[role_key] = app_id.lower()
    lshandler['LSHandlerPreferredVersions'] = { role_key: '-' }

    print 'Preparing to set "{}" as the default handler for "{}" with role "{}"'.format(
        app_id, uti, role
    )

    return lshandler


# Settings
current_username = get_current_username()
plist_name = 'com.apple.launchservices.secure.plist'
plist_rel_dir = 'Library/Preferences/com.apple.LaunchServices'
user_template_dir = '/System/Library/User Template/English.lproj'
lsregister = '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'

target_plists = [ os.path.join(user_template_dir, plist_rel_dir, plist_name) ]

if current_username:
    target_plists.append(os.path.join(
        '/Users', current_username, plist_rel_dir, plist_name
    ))


# Process plists
for target_plist in target_plists:
    print 'Working on plist "{}"'.format(target_plist)
    # Generate plist of default apps to add
    new_ls = []
    for setting in settings:
        print setting
        lshandler = gen_lshandler(app_id, setting[0], setting[1])
        new_ls.append(lshandler)

    # Generate plist of current default apps excluding ones we need to overwrite
    current_ls = read_binary_plist(target_plist)
    transfer_ls = []
    for ls in current_ls['LSHandlers']:
        # Get UTI and check for URL
        is_url = False
        try:
            uti = ls['LSHandlerContentType']
        except KeyError as e:
            uti = ls['LSHandlerURLScheme']
            is_url = True

        # Get role
        if is_url:
            role = 'url'
        else:
            role = ls['LSHandlerPreferredVersions'].keys()[0][13:].lower()

        # Format so we can compare it to the submitted settings
        setting = [uti, role]
        print 'Comparing [{}, {}]'.format(uti, role)
        if setting not in settings:
            print '--Transfering to new plist'
            transfer_ls.append(ls)
        else:
            print '--Not transfering, setting is being replaced'

    # Merge new LSHandlers and existing LSHandlers we can keep and write to tmp file
    to_write_ls = { 'LSHandlers': transfer_ls + new_ls}

    write_binary_plist(to_write_ls, target_plist)

# Rebuild launch services
rebuild_command = '{} -kill -r -domain local -domain system -domain user'.format(lsregister)
subprocess.check_output(rebuild_command.split())

import imp, os

from test_settings import THIS_FILE

msda = imp.load_source('msda', os.path.join(
	THIS_FILE, '../payload/msda')
)

# Sample LSHandlers
html_viewer_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='public.html',
	role='viewer'
)

https_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='https',
)

url_all_lshandler = msda.LSHandler(
	app_id='com.company.fakebrowser',
	uti='public.url',
)

# Functions
def protocol_lshandler_dict(app_id, uti):
	role_key = 'LSHandlerRoleAll'
	dict_ = {
		'LSHandlerURLScheme': uti.lower(),
		role_key: app_id,
		'LSHandlerPreferredVersions': {
			role_key: '-',
		}
	}
	return dict_

def uti_lshandler_dict(app_id, uti, role='all'):
	role_key = 'LSHandlerRole' + role.capitalize()
	dict_ = {
		'LSHandlerContentType': uti,
		role_key: app_id,
		'LSHandlerPreferredVersions': {
			role_key: '-',
		}
	}
	return dict_

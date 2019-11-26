# Mac Set Default Apps (MSDA)

MSDA provides an easy way to silently change the default applications used by macOS. There are no pop-ups or prompts and, even better, it works for Google Chrome!

## Requirements
* macOS 10.14.0 or newer
* Python 2 (which, for now, comes pre-installed on macOS)

## Deploying
### As a Local Installation
1. Download the latest packaged release of MSDA [here](https://github.com/targendaz2/Mac-Set-Default-Apps/releases)
2. Install the package on as many target Macs as needed, either manually or through a system such as Munki or Jamf

### As a Jamf Script
**Note:** I assume these instructions will also work for MDM services other than Jamf, I just only have familiarity with Jamf

1. Copy the contents of [payload/msda.py](https://github.com/targendaz2/Mac-Set-Default-Apps/blob/master/payload/msda.py) into a new Jamf script
2. Set the `JAMF` variable to `True` in the User-Editable Settings section

## Usage
**Note:** If using MSDA as a Jamf script, you would add these arguments in the Parameter 4 text field when assigning the script to a policy, excluding the initial `msda`

### Base Usage
```
msda command -h --version
```

* command can only be the following, for now
    * set: Set an application as a default
* -h, --help: Show MSDA's help message
* --version: Print the current version of MSDA

### Set Command Usage
**Note:** The computer will need to be restarted after using the `set` command in order to apply the changes

**Note:** This command must be run with administrative privileges

```
msda set [-h] [-fut] [-p PROTOCOL] [-u UTI ROLE] app_id
```

* app_id: The ID of the application to set as a default app
* -h, --help: Show help for the `set` command
* -feu: Apply the specified changes to all existing users
* -fut: Apply the specified changes to the `English.lproj` user template in addition to the currently logged on user (if there is one)
* -p, --protocol: Specify a protocol that the specified app should handle
* -u, --uti:
    * UTI: Specifiy a UTI that the specified app should handle
    * ROLE: The scenario under which the specified app should handle this UTI

### Examples

Set Google Chrome as the default web browser for the current user and the user template
```
msda set com.google.chrome -p http -p https -u public.url all -u public.html viewer -u public.xhtml all -fut
```

Set Microsoft Outlook as the default email client for the current user and the user template
```
msda set com.microsoft.outlook -p mailto -fut
```

Set Adobe Acrobat as the default PDF reader for the current user only
```
msda set com.adobe.acrobat.pro -u com.adobe.pdf all
```

Set Google Chrome as the default web browser and email client for the current user and the user template
```
msda set com.google.chrome -p http -p https -p mailto -u public.url all -u public.html viewer -u public.xhtml all -fut
```

## FAQ

How can I find an application's ID?
> Run `osascript -e 'id of app "Name of App"'` in a Terminal window, replacing the text between the double quotes with the name of the application in question.

How can I figure out what protocols or UTIs to set?
> I've tried to include the most common examples above. Otherwise, a complete list of protocols can be found [here](https://en.wikipedia.org/wiki/List_of_URI_schemes), and UTIs [here](https://escapetech.eu/manuals/qdrop/uti.html).

Are there commands other than `set`?
> At the moment, no. Please [create an issue](https://github.com/targendaz2/Mac-Set-Default-Apps/issues/new) on this app's GitHub page if there are commands you'd find useful.

Where can I go for help with this app?
> If you need help with this app specifically, please feel free to [create an issue](https://github.com/targendaz2/Mac-Set-Default-Apps/issues/new) on this app's GitHub page. I'll try to either respond, or implement changes to the app as soon as possible.

What about help with other Mac-related things?
>[Jamf Nation](https://www.jamf.com/jamf-nation/), the [MacSysAdmin subreddit](https://www.reddit.com/r/macsysadmin/), and the [MacAdmins Slack channel](https://macadmins.slack.com) are all great resources for help managing Macs in an enterprise environment.

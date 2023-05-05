# Mac Set Default Apps (MSDA)

MSDA provides an easy way to silently change the default applications used by macOS. There are no pop-ups or prompts and, even better, it works for Google Chrome!

## Requirements
* macOS >= 13.0.0, < 14.0.0

## Deploying
### As a Local Installation
1. Download the latest packaged release of MSDA [here](https://github.com/targendaz2/Mac-Set-Default-Apps/releases)
2. Install the package on as many target Macs as needed, either manually or through a system such as Munki or Jamf

### As a Jamf Script
1. Copy the contents of [payload/msda.py](https://github.com/targendaz2/Mac-Set-Default-Apps/blob/master/payload/msda.py) into a new Jamf script.
2. In the script's User-Editable Settings section, set the `JAMF` variable to `True`.

### As an Intune Script
1. Copy the contents of [payload/msda.py](https://github.com/targendaz2/Mac-Set-Default-Apps/blob/master/payload/msda.py) into a new Intune script.
2. In the script's User-Editable Settings section, set the `JAMF` variable to `True`.

## Usage
**Note:** If using MSDA as a Jamf script, add these arguments in the Parameter 4 text field when assigning the script to a policy, excluding the initial `msda`

### Base Usage
```
msda command -h --version
```

* command can only be the following, for now
    * set: Set an application as a default
* -h, --help: Show MSDA's help message
* --version: Print the current version of MSDA

### Set Command Usage
**Note:** The `set` command must be run with administrative privileges

```
msda set [-h,--help] [-feu] [-fut] [--browser app_id]
```

* app_id: The ID of the application to set as a default app
* -h, --help: Show help for the `set` command
* -feu: Apply the specified changes to all existing users
* -fut: Apply the specified changes to the `English.lproj` user template in addition to the currently logged on user (if there is one)

### Examples

Set Google Chrome as the default web browser for the current user and the user template
```
msda set --browser com.google.chrome -fut
```

Set Microsoft Outlook as the default email and calendar client for all existing users and the user template
```
msda set --mail com.microsoft.outlook --calendar com.microsoft.outlook -feu -fut
```

Set Adobe Acrobat as the default PDF reader for the current user only
```
msda set --pdf com.adobe.acrobat.pro
```

Set Microsoft Edge as the default web browser for just the current user
```
msda set --browser com.microsoft.edgemac
```

Set Google Chrome as the default web browser and email client for the current user and the user template
```
msda set --browser com.google.chrome --mail -fut
```

## FAQ

How can I find an application's ID?
> Run `osascript -e 'id of app "Name of App"'` in a Terminal window, replacing the text between the double quotes with the name of the application in question.

Where can I go for help with this app?
> If you need help with this app specifically, please feel free to [create an issue](https://github.com/targendaz2/Mac-Set-Default-Apps/issues/new) on this app's GitHub page. I'll try to either respond, or implement changes to the app as soon as possible.

What about help with other Mac-related things?
>[Jamf Nation](https://www.jamf.com/jamf-nation/), the [MacSysAdmin subreddit](https://www.reddit.com/r/macsysadmin/), and the [MacAdmins Slack channel](https://macadmins.slack.com) are all great resources for help managing Macs in an enterprise environment.

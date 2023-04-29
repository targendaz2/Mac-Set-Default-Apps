# Mac Set Default Apps (MSDA)

MSDA provides an interface for changing the default applications set in macOS.

## Requirements
* macOS 13.0.0
* Local admin access on the target device(s)

## Deploying
**Note:** MSDA can no longer be used as a Jamf script. Instead, it must be installed locally.
1. Download the latest packaged release of MSDA [here](https://github.com/targendaz2/Mac-Set-Default-Apps/releases)
2. Install the package on as many target Macs as needed, either manually or through a system such as Munki or Jamf

## Usage
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
msda set [-h] [-feu] [-fut] app_id app_role
```

* app_id: The ID of the application to set as a default app
* app_role: The role the application should fill
* -h, --help: Show help for the `set` command
* -feu: Apply the specified changes to all existing users
* -fut: Apply the specified changes to the `English.lproj` user template in addition to the currently logged on user (if there is one)

### Examples

Set Google Chrome as the default web browser for the current user and the user template
```
msda set com.google.chrome browser -feu -fut
```

Set Microsoft Outlook as the default email and calendar client for all existing users and the user template
```
msda set com.microsoft.outlook browser -feu -fut
msda set com.microsoft.outlook mail -feu -fut
```

Set Adobe Acrobat as the default PDF reader for the current user only
```
msda set com.adobe.acrobat.pro pdf
```

Set Microsoft Edge as the default web browser for just the current user
```
msda set com.microsoft.edgemac browser
```

Set Google Chrome as the default web browser and email client for the current user and the user template
```
msda set com.google.chrome browser -fut
msda set com.google.chrome mail -fut
```

## FAQ

How can I find an application's ID?
> Run `osascript -e 'id of app "Name of App"'` in a Terminal window, replacing the text between the double quotes with the name of the application in question.

Where can I go for help using this app?
>The app's error messages are a great place to start. They should be descriptive enough to get you on the right track. Otherwise, I don't have the capacity to help with general usage of this app, so I recommend seeking help in communities dedicated to managing macOS. These include [Jamf Nation](https://www.jamf.com/jamf-nation/), the [MacSysAdmin subreddit](https://www.reddit.com/r/macsysadmin/), and the [MacAdmins Slack channel](https://macadmins.slack.com).

What if I've found a bug in the app?
> Please [create an issue](https://github.com/targendaz2/Mac-Set-Default-Apps/issues/new) on this app's GitHub page including the command you're using, the goal you're trying to achieve, and the behavior you're observing.

What about help with other Mac-related things?
>[Jamf Nation](https://www.jamf.com/jamf-nation/), the [MacSysAdmin subreddit](https://www.reddit.com/r/macsysadmin/), and the [MacAdmins Slack channel](https://macadmins.slack.com) are all great resources for help managing Macs in an enterprise environment.

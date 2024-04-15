# Mac Set Default Apps (MSDA)

![GitHub License](https://img.shields.io/github/license/targendaz2/Mac-Set-Default-Apps)
![version](https://img.shields.io/github/package-json/v/targendaz2/Mac-Set-Default-Apps/jxa-v2?label=version)
![tests](https://github.com/targendaz2/Mac-Set-Default-Apps/actions/workflows/test.yml/badge.svg?branch=jxa-v2)

MSDA provides an easy way to silently change the default applications used by macOS. There are no pop-ups or prompts and, even better, it works for Google Chrome!

## Requirements

macOS Ventura (13.0) or newer

## Deploying

### Using Jamf Pro

1. Copy the contents of [payload/msda.py](https://github.com/targendaz2/Mac-Set-Default-Apps/blob/master/payload/msda.py) into a new Jamf script.
2. In the script's User-Editable Settings section, set the `JAMF` variable to `True`.

### As a Script via MDM

### As a Package via MDM

### Locally

## Usage

**Note:** If using MSDA as a Jamf script, add these arguments in the Parameter 4 text field when assigning the script to a policy, excluding the initial `msda`

### Base Usage

```bash
msda command -h --version
```

- command can only be the following, for now
  - set: Set an application as a default
- -h, --help: Show MSDA's help message
- --version: Print the current version of MSDA

### Set Command Usage

**Note:** The `set` command must be run with administrative privileges

```bash
msda set [-h] [-feu] [-fut] [-e EXTENSION ROLE] [-p PROTOCOL] [-u UTI ROLE] app_id
```

- app_id: The ID of the application to set as a default app
- -h, --help: Show help for the `set` command
- -feu: Apply the specified changes to all existing users
- -fut: Apply the specified changes to the `English.lproj` user template in addition to the currently logged on user (if there is one)
- -e, --extension:
  - EXTENSION: Specify a file extension that the specified app should handle
  - ROLE: The scenario under which the specified app should handle this UTI
- -p, --protocol: Specify a protocol that the specified app should handle
- -u, --uti:
  - UTI: Specify a UTI that the specified app should handle
  - ROLE: The scenario under which the specified app should handle this UTI

### Examples

Set Google Chrome as the default web browser for the current user and the user template

```bash
msda set com.google.chrome -p http -p https -u public.url all -u public.html viewer -u public.xhtml all -fut
```

Set Microsoft Outlook as the default email and calendar client for all existing users and the user template

```bash
msda set com.microsoft.outlook -p mailto -p webcal -u com.apple.ical.ics all -u com.apple.ical.vcs all -feu -fut
```

Set Adobe Acrobat as the default PDF reader for the current user only

```bash
msda set com.adobe.acrobat.pro -u com.adobe.pdf all
```

Set Microsoft Edge as the default web browser for just the current user

```bash
msda set com.microsoft.edgemac -p http -p https -u public.url all -u public.html viewer -u public.xhtml all
```

Set Google Chrome as the default web browser and email client for the current user and the user template

```bash
msda set com.google.chrome -p http -p https -p mailto -u public.url all -u public.html viewer -u public.xhtml all -fut
```

## Contributing

## FAQ

How can I find an application's ID?

> Run `osascript -e 'id of app "Name of App"'` in a Terminal window, replacing the text between the double quotes with the name of the application in question.

Where can I go for help with this app?

> If you need help with this app specifically, please feel free to [create an issue](https://github.com/targendaz2/Mac-Set-Default-Apps/issues/new) on this app's GitHub page. I'll try to either respond, or implement changes to the app as soon as possible.

What about help with other Mac-related things?

> [Jamf Nation](https://www.jamf.com/jamf-nation/), the [MacSysAdmin subreddit](https://www.reddit.com/r/macsysadmin/), and the [MacAdmins Slack channel](https://macadmins.slack.com) are all great resources for help managing Macs in an enterprise environment.

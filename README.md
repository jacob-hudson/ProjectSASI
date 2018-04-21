# ProjectSASI

[![Build Status](https://travis-ci.org/jacob-hudson/ProjectSASI.svg?branch=master)](https://travis-ci.org/jacob-hudson/ProjectSASI)

Splunk Alerts for Slack - Improved
Includes:
- Better formatting
- Easy standardization
- Automatic screenshots of visualizations

## Requirements
- `Slack Webhook Token` - For all standard alert features
- `Slack Bot User Token` - For screenshots
- `Full Python 2.7 install (System Python can work)` on the search head- For screenshots
- `Selenium via Pip (pip install selenium)` on the sarach head- For screenshots
- `PhantomJS` on the search head - For screenshots

## Build
### Pre-Built Packages
- [here](https://github.com/jacob-hudson/ProjectSASI/releases)

### Manual Build
- Download/Clone Repo (please ensure you are using a tagged commit)
- Run `./build/build.sh`

## Install
- `Install From File` in App Settings (App is not on SplunkBase yet)
- NOTE:  A restart is *not* needed after installing or upgrading this app

## Example Output
### Simple Alert
![Example Slack Alerts](https://github.com/jacob-hudson/ProjectSASI/blob/master/data/img/example.png?raw=true "Example Slack Alerts")

### CSV File
![Example Slack Alerts](https://github.com/jacob-hudson/ProjectSASI/blob/master/data/img/example_csv.png?raw=true "Example Slack Alerts - CSV")

## Known Bugs
- Dropdowns for Color and Emoji do not work (workaround: write in the color or emoji into the textbok for custom)

## Find an issue?
- Please report it ![here](https://github.com/jacob-hudson/ProjectSASI/issues/new "here")

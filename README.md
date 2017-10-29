# ProjectSASI

[![Build Status](https://travis-ci.org/jacob-hudson/ProjectSASI.svg?branch=master)](https://travis-ci.org/jacob-hudson/ProjectSASI)

Splunk Alerts for Slack - Improved
Includes:
- Better formatting
- Easy standardization
- Automatic screenshots of visualizations

## Requirements
- `Slack Webhook Token` - For all standard alert features
- `Slack API Token` - For screenshots

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

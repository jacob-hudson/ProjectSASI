#!/usr/bin/env bash

set -eufo pipefail

tar -cvzf slack_clean.tgz sai/

python build/convert.py

tar -cvzf slack_overwrite.tgz slack_alerts/

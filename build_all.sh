#!/usr/bin/env bash

set -eufo pipefail

tar -cvzf slack_overwrite.tgz slack_alerts/

tar -cvzf slack_clean.tgz sai/

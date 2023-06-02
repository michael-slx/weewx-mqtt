#!/usr/bin/env bash
set -e

SOURCE_DIR="/vagrant"

if [[ -d "/usr/lib/weewx/user" ]]; then
    sudo wee_extension --install="$SOURCE_DIR"
elif [[ -d "$HOME/weewx-data/bin/user" ]]; then
    weectl extension install "$SOURCE_DIR"
else
    echo "Could not determine target directory"
    echo "Have you installed WeeWX?"
    exit 2
fi

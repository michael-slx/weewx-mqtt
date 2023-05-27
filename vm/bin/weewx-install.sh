#!/usr/bin/env bash

set -e

PACKAGES=(
    "weewx"
    "python-pyephem"
)

yay -S --noconfirm "${PACKAGES[@]}"

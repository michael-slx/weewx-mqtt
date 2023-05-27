#!/usr/bin/env bash

set -e

PACKAGES=(
  "python"
  "python-pip"
  "python-paho-mqtt"
  "mosquitto"
)
PATH_ENTRIES=(
  "$HOME/.local/bin"
  "/vagrant/vm/bin"
)

MQTT_WEEWX_PASSWD="passwd-mqtt-1234"

yay -Syyuu --noconfirm "${PACKAGES[@]}" 

for path_entry in "${PATH_ENTRIES[@]}"; do
  export_str="export PATH=\"${path_entry}:\${PATH}\""
  if ! grep -q "$export_str" "/home/vagrant/.zshrc" >/dev/null; then
    echo "Adding \"$path_entry\" to \$PATH"
    echo "$export_str" >> /home/vagrant/.zshrc
  fi
done

sudo cp -R "/vagrant/vm/conf/mosquitto"/* "/etc/mosquitto"
sudo mosquitto_passwd -c -b "/etc/mosquitto/passwd" "weewx" "$MQTT_WEEWX_PASSWD"
sudo systemctl enable --now mosquitto.service

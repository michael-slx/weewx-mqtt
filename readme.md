# Note

This project is **no longer supported**. Use [**matthewwall/weewx-mqtt**](https://github.com/matthewwall/weewx-mqtt) instead.

# MQTT addon for WeeWX

Extension for WeeWX that allows publishing LOOP records to an MQTT broker.

This extension requires **Python 3**, **WeeWX 4** and the **Paho MQTT** library.

## Contents

- [Contents](#contents)
- [Installation](#installation)
- [Contribution](#contribution)
- [Legal](#legal)

## Installation

1. Ensure you are using **Python 3** and **WeeWX 4**. You'll also need to have set up an MQTT broker.
2. Install the **Paho MQTT** library:

E.g.:

```sh
# Debian, Ubuntu, Raspberry Pi OS
$ sudo apt install python3-paho-mqtt
```

Or:

```sh
# Fedora
$ sudo dnf install python3-paho-mqtt
```

Or:

```sh
# Arch
$ sudo pacman -S python-paho-mqtt
```

Or:

```sh
# pip
$ sudo pip3 install paho-mqtt
```

3. Download the release file from this repository.
4. Install the extension using the `wee_extension` utility:

E.g.:

```sh
# Replace file name with actual path of downloaded file
$ sudo wee_extension --install weewx-mqtt.tar.xz
```

5. Open the WeeWX configuration file in your favorite text editor:

E.g.:

```sh
$ sudo nano /etc/weewx/weewx/conf
```

6. Find the `[StdRESTful]` section and navigate to the `[[MQTT]]` section within it.
7. Edit the configuration options according to your needs:

```ini
    # Configuration for uploading LOOP data to an MQTT broker
    [[MQTT]]

        # Enable/disable this service
        enable = true

        # Hostname/IP of MQTT broker
        host = localhost

        # Credentials
        # Leave blank or uncomment for anonymous authentication
        #user =
        #password =

        # Prefix for topics
        topic = weather
```

8. Save the edited configuration
9. Start or restart WeeWX

## Contribution

Any contributions to this project are absolutely welcome: issues, documentation and even pull requests.

## Legal

This project is licensed under the Apache License, Version 2.0. See the [`LICENSE` file](LICENSE) for a copy of the license.

All trademarks are held by their respective owners.

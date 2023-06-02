# Copyright 2023 Michael Schantl and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Optional

import configobj

from weeutil.weeutil import to_bool, to_int
from weewx.restx import get_site_dict
from weewx.units import unit_constants

_KEY_SITE = "MQTT"
_KEY_HOST = "host"
_KEY_PORT = "port"
_KEY_USER = "user"
_KEY_PASSWORD = "password"
_KEY_TOPIC = "topic"
_KEY_UNIT_SYSTEM = "unit_system"
_KEY_LOG_SUCCESS = "log_success"
_KEY_LOG_FAILURE = "log_failure"


def _get_str_or_empty(conf_dict: dict, key: str) -> Optional[str]:
    value = conf_dict.get(key)
    return str(value) if value and str(value.strip()) else None


def _get_int_or_empty(conf_dict: dict, key: str) -> Optional[int]:
    value = conf_dict.get(key)
    return to_int(value) if value and str(value.strip()) else None


class Configuration(object):
    def __init__(self,
                 log_success: bool,
                 log_failure: bool,
                 host: str,
                 port: Optional[int],
                 user: Optional[str],
                 password: Optional[str],
                 topic: Optional[str],
                 unit_system: Optional[str]):
        super().__init__()

        self.log_success = log_success
        self.log_failure = log_failure
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.topic = topic
        self.unit_system = unit_system

    @staticmethod
    def create_from_config(config: configobj.ConfigObj) -> Optional["Configuration"]:
        site_dict = get_site_dict(config, _KEY_SITE, _KEY_HOST)
        if not site_dict:
            return None

        log_success = to_bool(site_dict[_KEY_LOG_SUCCESS])
        log_failure = to_bool(site_dict[_KEY_LOG_FAILURE])

        host = site_dict[_KEY_HOST]
        port = _get_int_or_empty(site_dict, _KEY_PORT)

        user = _get_str_or_empty(site_dict, _KEY_USER)
        password = _get_str_or_empty(site_dict, _KEY_PASSWORD)

        topic = _get_str_or_empty(site_dict, _KEY_TOPIC)

        unit_system = _get_str_or_empty(site_dict, _KEY_UNIT_SYSTEM)

        return Configuration(
            log_success=log_success,
            log_failure=log_failure,
            host=host,
            port=port,
            user=user,
            password=password,
            topic=topic,
            unit_system=unit_system,
        )

    @property
    def unit_system_int(self) -> Optional[int]:
        return unit_constants[self.unit_system] if self.unit_system is not None else None

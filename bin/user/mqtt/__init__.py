import logging
import queue
import random
import socket
from typing import Optional

import paho.mqtt.client
from paho.mqtt.client import Client as MqttClient

import weewx.restx
from user.mqtt.configuration import Configuration
from weewx.units import to_std_system

log = logging.getLogger(__name__)


def _mask_password(password: str) -> str:
    password_len = len(password)
    return "*" * password_len


class MqttService(weewx.restx.StdRESTful):
    def __init__(self, engine, config_dict):
        super().__init__(engine, config_dict)

        self.config = Configuration.create_from_config(config_dict)

        if self.config:
            self.loop_queue = queue.Queue()
            self._initialize()

    def _log_success(self, message: str, level: int = logging.DEBUG) -> None:
        if not self.config or self.config.log_success:
            log.log(level, message)

    def _log_failure(self, message: str, level: int = logging.ERROR) -> None:
        if not self.config or self.config.log_failure:
            log.log(level, message)

    def _initialize(self) -> None:
        self._log_success("Initializing MQTT service")

        self.loop_thread = MqttThread(self.loop_queue, self.config)
        self.loop_thread.start()

        self.bind(weewx.NEW_LOOP_PACKET, self._on_loop_packet)

    def _on_loop_packet(self, event) -> None:
        packet = event.packet
        self._log_success("New loop packet: %s" % repr(packet))
        self.loop_queue.put(packet)


def _get_unit_key(observation_key: str, unit_system: int) -> str:
    unit = weewx.units.getStandardUnitType(unit_system, observation_key)
    return unit[0]


class MqttThread(weewx.restx.RESTThread):
    def __init__(self,
                 q: queue.Queue,
                 config: configuration.Configuration,
                 manager_dict: Optional[dict] = None):
        super().__init__(q,
                         protocol_name="MQTT",
                         manager_dict=manager_dict,
                         post_interval=None,
                         log_success=config.log_success,
                         log_failure=config.log_failure)
        self._client = self._create_client(config)
        self._topic = config.topic
        self._unit_system = config.unit_system_int

    def _create_client(self, config: configuration.Configuration) -> MqttClient:
        pad = "%032x" % random.getrandbits(128)
        client_id = 'weewx_%s' % pad[:8]

        self._log_success("Creating MQTT client with id \"%s\"" % client_id)
        client = MqttClient(client_id=client_id)

        if config.user and config.password:
            self._log_success(
                "Using MQTT credentials \"%s\" (password %s)" % (config.user, _mask_password(config.password)))
            client.username_pw_set(config.user, config.password)

        port = config.port if config.port is not None else 1883

        try:
            client.connect(config.host, port)

        except (socket.error, socket.timeout, socket.herror) as e:
            raise weewx.restx.ConnectError("Failed to connect to MQTT server %s:%d" % (config.host, port)) from e

        return client

    def _log_success(self, message: str, level: int = logging.DEBUG) -> None:
        if self.log_success:
            log.log(level, message)

    def _log_failure(self, message: str, level: int = logging.ERROR) -> None:
        if self.log_failure:
            log.log(level, message)

    def format_url(self, _):
        pass

    def run_loop(self, dbmanager=None):
        self._log_success("Starting MQTT client")
        self._client.loop_start()

        try:
            self._log_success("Entering upload thread loop")
            super().run_loop(dbmanager)
            self._log_success("Exited upload thread loop")

        finally:
            self._log_success("Stopping MQTT client")
            self._client.loop_stop()

    def process_record(self, record: dict, dbmanager) -> None:
        record_converted_units = to_std_system(record, self._unit_system) if self._unit_system is not None else record
        self._post_record(record_converted_units)

    def _post_record(self, record: dict) -> None:
        for key, value in record.items():
            unit_key = _get_unit_key(observation_key=key, unit_system=record['usUnits'])
            topic = self._build_topic(observation=key, unit=unit_key)

            self._log_success("Publishing \"%s\": %s (%s)" % (topic, str(value), unit_key))
            (status, _) = self._client.publish(topic, value)

            if status != paho.mqtt.client.MQTT_ERR_SUCCESS:
                self._log_failure("Publish failed for \"%s\": %s" % (str(topic), paho.mqtt.client.error_string(status)))

    def _build_topic(self, observation: str, unit: Optional[str] = None) -> str:
        observation_key = f"{observation}_{unit}" if unit else observation

        if self._topic:
            return f"{self._topic}/{observation_key}"
        else:
            return observation_key

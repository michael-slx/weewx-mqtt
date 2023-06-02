import configobj

from weecfg.extension import ExtensionInstaller, ExtensionEngine


def loader() -> ExtensionInstaller:
    return MqttInstaller()


class MqttInstaller(ExtensionInstaller):
    def __init__(self) -> None:
        super().__init__(
            version="0.1.0",
            name='MQTT',
            description="Extension for uploading LOOP data to an MQTT broker",
            author='Michael Schantl',
            author_email="michael@schantl-lx.at",
            restful_services='user.mqtt.MqttService',
            files=[
                ('bin/user/mqtt', [
                    'bin/user/mqtt/__init__.py',
                    'bin/user/mqtt/configuration.py',
                ])
            ],
        )

    def configure(self, engine: ExtensionEngine) -> bool:
        config_dict: configobj.ConfigObj = engine.config_dict
        if 'StdRESTful' in config_dict and 'MQTT' in config_dict['StdRESTful']:
            return False

        mqtt_config = {
            "enable": "false",
            "host": "replace_me",
            "user": "replace_me",
            "password": "replace_me",
            "topic": "replace_me",
        }
        config_dict['StdRESTful']['MQTT'] = mqtt_config

        config_dict['StdRESTful'].comments['MQTT'] = ["", "Configuration for uploading LOOP data to an MQTT broker"]
        config_dict['StdRESTful']['MQTT'].comments['enable'] = ["", "Enable/disable this service"]
        config_dict['StdRESTful']['MQTT'].comments['host'] = ["", "Hostname/IP of MQTT broker"]
        config_dict['StdRESTful']['MQTT'].comments['user'] = ["", "Credentials"]
        config_dict['StdRESTful']['MQTT'].comments['topic'] = ["", "Prefix for topics"]

        return True

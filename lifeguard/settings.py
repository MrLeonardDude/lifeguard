"""
Lifeguard core settings
"""
import sys
from os import environ


class SettingsManager(object):
    def __init__(self, settings):
        self.settings = settings

        for entry in self.settings:
            setattr(self, "__{}".format(entry.lower()), self.__get_value(entry))

    def __get_value(self, name):
        options = self.settings[name]
        return environ.get(name, options["default"])

    def read_value(self, name):
        return getattr(self, "__{}".format(name.lower()))

    def load_class(self, name):
        value = self.__get_value(name)
        if value:
            package_path = value.split(".")
            class_name = package_path.pop(-1)
            return getattr(__import__(".".join(package_path)), class_name)
        return value


SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_DIRECTORY": {
            "default": "/data/lifeguard",
            "description": "Location of validations and others resources",
        },
        "LIFEGUARD_LOG_LEVEL": {
            "default": "INFO",
            "description": "Sets the Lifeguard's core log level",
        },
        "LIFEGUARD_VALIDATION_REPOSITORY_IMPLEMENTATION": {
            "default": None,
            "description": "Full package path to validation implementation class",
        },
    }
)

LIFEGUARD_DIRECTORY = SETTINGS_MANAGER.read_value("LIFEGUARD_DIRECTORY")
LOG_LEVEL = SETTINGS_MANAGER.read_value("LIFEGUARD_LOG_LEVEL")
VALIDATION_REPOSITORY_IMPLEMENTATION = SETTINGS_MANAGER.load_class(
    "LIFEGUARD_VALIDATION_REPOSITORY_IMPLEMENTATION"
)

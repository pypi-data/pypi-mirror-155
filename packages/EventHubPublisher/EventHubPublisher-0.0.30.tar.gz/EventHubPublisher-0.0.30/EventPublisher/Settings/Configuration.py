import os, JsonParser
from os.path import dirname, abspath
import Settings.SettingsDefaults as SettingsDefaults

class Configuration:
    def init(self, environment_name):
        if not environment_name in SettingsDefaults.ENVIRONMENTS:
            raise Exception(environment_name + " is not valid environment. Valid events are: " + JsonParser.serialize(SettingsDefaults.ENVIRONMENTS))
        if not os.getenv(SettingsDefaults.APP_ENVIRONMENT_KEY) is environment_name:
            os.environ[SettingsDefaults.APP_ENVIRONMENT_KEY] = environment_name
            self.read_settings()

    def get_environment(self):
        env = os.getenv(SettingsDefaults.APP_ENVIRONMENT_KEY)
        if not env or env is None:
            raise Exception("Environment is not set.")
        return env

    def get_environment_settings(self):
        settingsJson = os.getenv(SettingsDefaults.APP_ENVIRONMENT_SETTINGS_KEY)
        if not settingsJson or settingsJson is None:
            raise Exception("Environment settings are not set")
        settings = JsonParser.parse(settingsJson)

        return JsonParser.get_by_key(settings, self.get_environment())

    def read_settings(self):
        directoiry = dirname(dirname(dirname(abspath(__file__))))
        settings_file_path = os.path.join(directoiry, SettingsDefaults.SETTINGS_JSON_PATH)
        settings = JsonParser.parse_from_file(settings_file_path)
        self.set_environment_settings(settings)

    def set_environment_settings(self, settings):
        os.environ[SettingsDefaults.APP_ENVIRONMENT_SETTINGS_KEY] = JsonParser.serialize(settings)
        
    def get_connection_string(self):
        settings = self.get_environment_settings()
        return JsonParser.get_by_key(settings, SettingsDefaults.EVENTHUB_CONNECTION_STRING_KEY)

    def get_eventhub_name(self):
        settings = self.get_environment_settings()
        return JsonParser.get_by_key(settings, SettingsDefaults.EVENTHUB_NAME_KEY)

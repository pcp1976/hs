from interfaces import HSPlugin
from pluggy import HookimplMarker
from configobj import ConfigObj
import os

settings_storage = HookimplMarker("hs")


class Ini(HSPlugin):
    def __init__(self):
        super().__init__()
        self.config = ConfigObj()
        self.order = 2

    @settings_storage
    def settings_get_value(self, setting_name: str):
        if setting_name in self.config.keys():
            return self.config[setting_name]

    @settings_storage
    def settings_set_value(self, setting_name: str, setting_value):
        self.config[setting_name] = setting_value
        self.config.write()
        self.event(
            event_type="settings_set_value",
            event_data={"setting_name": setting_name, "setting_value": setting_value},
            event_metadata={},
        )

    def activate(self):
        configdir = self.pm.hook.filepath_get(plugin_name="settings_storage-ini")[0]
        self.config = ConfigObj(os.path.join(configdir, "config.ini"))

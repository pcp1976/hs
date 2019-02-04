from interfaces import HSPlugin
from dotenv import load_dotenv
import os
from pluggy import HookimplMarker

settings_storage = HookimplMarker("hs")

load_dotenv()


class DotEnv(HSPlugin):
    env_vars = os.environ

    def __init__(self):
        super().__init__()
        self.order = 10

    @settings_storage
    def settings_get_value(self, setting_name: str):
        return os.getenv(setting_name)

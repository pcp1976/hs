from interfaces import HSPlugin
from pluggy import HookimplMarker
import os

filepaths = HookimplMarker("hs")


class FilePaths(HSPlugin):
    base_path = os.path.join(os.getcwd(), "plugin_files")

    def __init__(self):
        super().__init__()
        self.order = 1

    @filepaths
    def filepath_get(self, plugin_name: str):
        expected_path = os.path.join(self.base_path, plugin_name)
        if not os.path.isdir(expected_path):
            os.mkdir(expected_path)
        return expected_path

    def activate(self):
        if not os.path.isdir(self.base_path):
            os.mkdir(self.base_path)

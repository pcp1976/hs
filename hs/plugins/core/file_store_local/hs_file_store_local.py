from interfaces import HSPlugin
from pluggy import HookimplMarker
import uuid
import os
from shutil import copyfile


hs_file_store = HookimplMarker("hs")


class FileStoreLocal(HSPlugin):
    name = "file_store_local"

    def __init__(self):
        super().__init__()
        self.order = 200
        self.base_dir = None

    def activate(self):
        self.base_dir = self.pm.hook.filepath_get(plugin_name=self.name)[0]
        self.event(
            event_type="storage_location_set",
            event_data={
                "location": self.base_dir,
                "storage_type": self.name
            },
            event_metadata={}
        )
        self.pm.hook.artefact_storage_register(storage_type=self.name)
        self.log.notice(f"activated {self.order}")

    def store_file(self, filepath)->str:
        filename = str(uuid.uuid1())
        copyfile(filepath, os.path.join(self.base_dir, filename))
        self.event(
            event_type="file_stored",
            event_data={
                "token": filename,
                "original_file": filepath,
                "storage_type": self.name
            },
            event_metadata={}
        )
        return filename

    # TODO this should be rewritten using the asyncio thread pattern from eventstore
    @hs_file_store
    def file_store(self, filepath: str, storage_type: str) -> str:
        """
        :param filepath: path of the file to store
        :param storage_type: to differentiate between different storage options
        :return: token to retrieve a file
        """
        if storage_type == self.name or self.pm.hook.settings_get_value(setting_name="DEFAULT_STORAGE")[0] == self.name:
            return self.store_file(filepath)
        else:
            return ""

    @hs_file_store
    def file_store(self, filepath: str) -> str:
        """
        :param filepath: path of the file to store
        :return: token to retrieve a file
        """
        if self.pm.hook.settings_get_value(setting_name="DEFAULT_STORAGE")[0] == self.name:
            return self.store_file(filepath)
        else:
            return ""

    @hs_file_store
    def file_retrieve(self, filepath: str, token: str):
        """
        :param filepath: where to put the retrieved file
        :param token: token identifier for file
        """
        copyfile(os.path.join(self.base_dir, token), filepath)
        self.event(
            event_type="file_retrieved",
            event_data={"path": filepath},
            event_metadata={}
        )

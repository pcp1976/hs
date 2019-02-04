from interfaces import HSPlugin
from pluggy import HookimplMarker


hs_file_store = HookimplMarker("hs")


class ArtifactStorage(HSPlugin):
    name = "artifact_store"

    def __init__(self):
        super().__init__()
        self.order = 150
        self.base_dir = None

    def activate(self):
        self.log.notice(f"activated {self.order}")

    @hs_file_store
    def artefact_storage_register(self, storage_type: str):
        self.pm.hook.create_subscription(
            stream_name=storage_type,
            subscription_name=self.name
        )
        self.pm.hook.register_event_handler(
            stream_name=storage_type,
            subscription_name=self.name,
            event_handler=self.raise_event
        )

    def raise_event(self, event_type, event_data, event_metadata):
        """
        :param event_type: type of the event
        :param event_data: the event data
        :param event_metadata: the event metadata
        :return: None
        """
        self.event(
            event_type=event_type,
            event_data=event_data,
            event_metadata=event_metadata
        )


from interfaces import HSPlugin
from pluggy import HookimplMarker
import os
import asyncio
from photonpump import connect as p_connect

eventstore = HookimplMarker("hs")


class EventStore(HSPlugin):
    base_path = os.path.join(os.getcwd(), "plugin_files")

    def __init__(self):
        super().__init__()
        self.photonpump_connection = None
        self.mainloop = asyncio.get_event_loop()

    def activate(self):
        self.photonpump_connection = asyncio.ensure_future(self.get_p(self.mainloop))
        self.mainloop.run_until_complete(self.photonpump_connection)
        self.pm.hook.log_notice(message="activated", plugin_name="eventstore")

    async def get_p(self, _mainloop):
        global client
        client = p_connect(
            host=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_URL")[0],
            port=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_TCP_PORT")[0],
            username=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_USER")[0],
            password=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_PASS")[0],
            loop=_mainloop,
        )
        await client.connect()

    @eventstore
    async def register_event_handler(self, stream_name, subscription_name, event_handler):
        """
        :param stream_name: name of the stream the event_handler receives events from
        :param subscription_name: identifier for the subscription
        :param event_handler: function which will receive events from the stream
        :return: None
        """
        pass

    @eventstore
    async def deregister_event_handler(self, event_handler):
        """
        :param event_handler: function which will no longer receive events from the stream
        :return: None
        """

    @eventstore
    async def delete_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to delete the subscription from
        :param subscription_name: identifier of the subscription to delete
        :return: None
        """
        pass

    @eventstore
    async def create_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to create the subscription on
        :param subscription_name: identifier for the subscription
        :return: None
        """
        await self.photonpump_connection.create_subscription(
            subscription_name,
            stream_name
        )

    @eventstore
    async def raise_event(self, stream_name: str, event_type: str, event_data: dict, event_metadata: dict):
        """
        :param stream_name: name of the stream to post event to
        :param event_type: type of the event
        :param event_data: the event data
        :param event_metadata: the event metadata
        :return: None
        """
        await self.photonpump_connection.publish_event(
            stream_name,
            event_type,
            body=event_data,
            metadata=event_metadata
        )

    @eventstore
    async def start_event_streams(self) -> bool:
        """
        Start up the event streams
        :return: bool True on success
        """
        pass

    @eventstore
    async def stop_event_streams(self) -> bool:
        """
        Stop event streams
        :return: bool True on success
        """
        pass

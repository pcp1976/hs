from interfaces import HSPlugin
from pluggy import HookimplMarker
import asyncio
from photonpump import connect as p_connect
from threading import Thread

eventstore = HookimplMarker("hs")


class EventStore(HSPlugin):
    """
    Phontonpump uses async to process calls to/from eventstore.
    To manage async creep (ie prevent the entire application from having to be wrapped in async decorators,
    and to only have the io-bound code in async) the async loop is wrapped in a thread.
    """

    name = "eventstore"

    def __init__(self):
        super().__init__()
        self.photonpump_connection = None
        self.loop = asyncio.new_event_loop()
        self.my_thread = None

    def activate(self):
        connect = asyncio.ensure_future(self.get_p(), loop=self.loop)
        self.loop.run_until_complete(connect)  # block here: connection or bust!
        # TODO: check we have a connection before continuing
        self.my_thread = Thread(target=self.start_background_loop, args=(self.loop,))
        self.my_thread.start()
        self.log.notice(f"activated {self.order}")

    @staticmethod
    def start_background_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def get_p(self):
        self.photonpump_connection = p_connect(
            host=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_URL")[0],
            port=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_TCP_PORT")[0],
            username=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_USER")[0],
            password=self.pm.hook.settings_get_value(setting_name="EVENTSTORE_PASS")[0],
            loop=self.loop,
        )
        await self.photonpump_connection.connect()

    @eventstore
    def register_event_handler(self, stream_name, subscription_name, event_handler):
        """
        :param stream_name: name of the stream the event_handler receives events from
        :param subscription_name: identifier for the subscription
        :param event_handler: function which will receive events from the stream
        :return: None
        """
        # TODO: remember to wrap so that
        #  a) the event looks like eventsource-memory's and
        #  b) the event is acknowledged upon completion of the handler
        pass

    @eventstore
    def deregister_event_handler(self, event_handler):
        """
        :param event_handler: function which will no longer receive events from the stream
        :return: None
        """

    @eventstore
    def delete_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to delete the subscription from
        :param subscription_name: identifier of the subscription to delete
        :return: None
        """
        pass

    @eventstore
    def create_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to create the subscription on
        :param subscription_name: identifier for the subscription
        :return: None
        """
        asyncio.run_coroutine_threadsafe(
            self.photonpump_connection.create_subscription(
                subscription_name, stream_name
            ),
            loop=self.loop,
        )

    @eventstore
    def raise_event(
        self, stream_name: str, event_type: str, event_data: dict, event_metadata: dict
    ):
        """
        :param stream_name: name of the stream to post event to
        :param event_type: type of the event
        :param event_data: the event data
        :param event_metadata: the event metadata
        :return: None
        """
        asyncio.run_coroutine_threadsafe(
            self.photonpump_connection.publish_event(
                stream_name, event_type, body=event_data, metadata=event_metadata
            ),
            loop=self.loop,
        )

    @eventstore
    def start_event_streams(self) -> bool:
        """
        Start up the event streams
        :return: bool True on success
        """
        pass

    @eventstore
    def stop_event_streams(self) -> bool:
        """
        Stop event streams
        :return: bool True on success
        """
        pass

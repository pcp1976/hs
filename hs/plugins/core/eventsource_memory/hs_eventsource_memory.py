from interfaces import HSPlugin
from pluggy import HookimplMarker


eventsource = HookimplMarker("hs")


class EventSourceMemory(HSPlugin):
    """
    Phontonpump uses async to process calls to/from eventstore.
    To manage async creep (ie prevent the entire application from having to be wrapped in async decorators,
    and to only have the io-bound code in async) the async loop is wrapped in a thread.
    """
    def __init__(self):
        super().__init__()
        self.streams = {}
        self.subscriptions = {}

    def activate(self):
        self.pm.hook.log_notice(
            plugin_name="eventsource_memory",
            message="activated"
        )
    @eventsource
    def register_event_handler(self, stream_name, subscription_name, event_handler):
        """
        :param stream_name: name of the stream the event_handler receives events from
        :param subscription_name: identifier for the subscription
        :param event_handler: function which will receive events from the stream
        :return: None
        """
        if event_handler not in self.subscriptions[stream_name][subscription_name]:
            self.subscriptions[stream_name][subscription_name].append(event_handler)
        self.pm.hook.log_trace(
            plugin_name="eventsource_memory",
            message=f"registered {event_handler} on {stream_name}:{subscription_name}"
        )

    @eventsource
    def deregister_event_handler(self, event_handler):
        """
        :param event_handler: function which will no longer receive events from the stream
        :return: None
        """

    @eventsource
    def delete_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to delete the subscription from
        :param subscription_name: identifier of the subscription to delete
        :return: None
        """
        pass

    @eventsource
    def create_subscription(self, stream_name, subscription_name):

        if stream_name not in self.streams:
            self.streams.update({stream_name: []})
        if stream_name not in self.subscriptions:
            self.subscriptions.update({stream_name: {}})
        if subscription_name not in self.subscriptions[stream_name]:
            self.subscriptions[stream_name].update({subscription_name: []})
        self.pm.hook.log_trace(
            message=f"self.subscriptions={self.subscriptions}",
            plugin_name="eventsource_memory"
        )
        self.pm.hook.log_trace(
            message=f"self.streams={self.streams}",
            plugin_name="eventsource_memory"
        )

    @eventsource
    def raise_event(self, stream_name: str, event_type: str, event_data: dict, event_metadata: dict):
        event = {
            "event_type": event_type,
            "event_data": event_data,
            "event_metadata": event_metadata
        }
        self.streams[stream_name].append(event)
        for sub in self.subscriptions[stream_name]:
            for callback in self.subscriptions[stream_name][sub]:
                self.pm.hook.log_debug(
                    plugin_name="eventsource_memory",
                    message=f"calling {callback} with {event}"
                )
                callback(event)

    @eventsource
    def start_event_streams(self) -> bool:
        """
        Start up the event streams
        :return: bool True on success
        """
        pass

    @eventsource
    def stop_event_streams(self) -> bool:
        """
        Stop event streams
        :return: bool True on success
        """
        pass

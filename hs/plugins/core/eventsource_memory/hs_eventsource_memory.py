from interfaces import HSPlugin
from pluggy import HookimplMarker


eventsource = HookimplMarker("hs")


class EventSourceMemory(HSPlugin):
    """
    Simple, volatile event source using dicts
    """

    name = "eventsource_memory"

    def __init__(self):
        super().__init__()
        self.streams = {}
        self.subscriptions = {}
        self.order = 4

    def activate(self):
        self.log.notice(f"activated {self.order}")

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
        self.log.trace(
            f"registered {event_handler} on {stream_name}:{subscription_name}"
        )

    @eventsource
    def deregister_event_handler(self, event_handler):
        """
        :param event_handler: function which will no longer receive events from the stream
        :return: None
        """
        for stream in self.subscriptions:
            for sub in self.subscriptions[stream]:
                if event_handler in self.subscriptions[stream][sub]:
                    self.subscriptions[stream][sub].remove(event_handler)

    @eventsource
    def delete_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to delete the subscription from
        :param subscription_name: identifier of the subscription to delete
        :return: None
        """
        if subscription_name in self.subscriptions[stream_name]:
            self.subscriptions[stream_name].remove(subscription_name)

    @eventsource
    def create_subscription(self, stream_name, subscription_name):

        if stream_name not in self.streams:
            self.streams.update({stream_name: []})
        if stream_name not in self.subscriptions:
            self.subscriptions.update({stream_name: {}})
        if subscription_name not in self.subscriptions[stream_name]:
            self.subscriptions[stream_name].update({subscription_name: []})
        self.log.trace(f"self.subscriptions={self.subscriptions}")
        self.log.trace(f"self.streams={self.streams}")

    @eventsource
    def raise_event(
        self, stream_name: str, event_type: str, event_data: dict, event_metadata: dict
    ):
        if stream_name not in self.streams:
            self.streams[stream_name] = []
        event = {
            "event_type": event_type,
            "event_data": event_data,
            "event_metadata": event_metadata,
        }
        self.streams[stream_name].append(event)
        try:
            for sub in self.subscriptions[stream_name]:
                for callback in self.subscriptions[stream_name][sub]:
                    self.log.debug(f"calling {callback} with {event}")
                    callback(event)
        except KeyError:
            self.log.error(f"no subscriptions for stream '{stream_name}'")

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

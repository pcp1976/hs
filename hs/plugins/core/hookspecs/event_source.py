from pluggy import HookspecMarker


event_source = HookspecMarker("hs")


class EventSource:
    @event_source
    def register_event_handler(self, stream_name, subscription_name, event_handler):
        """
        :param stream_name: name of the stream the event_handler receives events from
        :param subscription_name: identifier for the subscription
        :param event_handler: function which will receive events from the stream
        :return: None
        """
        pass

    @event_source
    def deregister_event_handler(self, event_handler):
        """
        :param event_handler: function which will no longer receive events from the stream
        :return: None
        """

    @event_source
    def delete_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to delete the subscription from
        :param subscription_name: identifier of the subscription to delete
        :return: None
        """
        pass

    @event_source
    def create_subscription(self, stream_name, subscription_name):
        """
        :param stream_name: name of the stream to create the subscription on
        :param subscription_name: identifier for the subscription
        :return: None
        """
        pass

    @event_source
    def raise_event(self, stream_name, event_type, event_data, event_metadata):
        """
        :param stream_name: name of the stream to post event to
        :param event_type: type of the event
        :param event_data: the event data
        :param event_metadata: the event metadata
        :return: None
        """
        pass

    @event_source
    def start_event_streams(self) -> bool:
        """
        Start up the event streams
        :return: bool True on success
        """
        pass

    @event_source
    def stop_event_streams(self) -> bool:
        """
        Stop event streams
        :return: bool True on success
        """
        pass

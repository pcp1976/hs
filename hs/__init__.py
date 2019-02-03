from composer import Composer


def main():
    manager = Composer()
    manager.collect_plugins()
    manager.activate_plugins()
    manager.pm.hook.create_subscription(
        stream_name="test",
        subscription_name="sub test"
    )
    manager.pm.hook.register_event_handler(
        stream_name="test",
        subscription_name="sub test",
        event_handler=e_handler
    )
    manager.pm.hook.raise_event(
        stream_name="test",
        event_type="download_request",
        event_data={
            "source_url": "http://google.com",
            "destination": "a_file.html"
        },
        event_metadata={
            "originator": "Paul"
        }
    )


def e_handler(event):
    print(event)


if __name__ == "__main__":
    main()

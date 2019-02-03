from composer import Composer


def main():
    manager = Composer()
    manager.collect_plugins()
    manager.activate_plugins()
    manager.pm.hook.create_subscription(
        stream_name="test",
        subscription_name="sub test"
    )


if __name__ == "__main__":
    main()

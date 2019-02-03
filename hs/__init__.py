from composer import Composer


def main():
    manager = Composer()
    manager.collect_plugins()
    manager.activate_plugins()


if __name__ == "__main__":
    main()

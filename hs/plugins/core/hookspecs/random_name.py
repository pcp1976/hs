from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


@hs_hookspec
def get_random_name():
    """
    In the spirit of Docker's wonderfully whimsical random container names...
    :return: str - a random name
    """
    pass

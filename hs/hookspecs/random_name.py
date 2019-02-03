from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


class RandomName:
    @hs_hookspec
    def get_random_name(self):
        """
        In the spirit of Docker's wonderfully whimsical random container names...
        :return: str - a random name
        """
        pass

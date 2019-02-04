from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


@hs_hookspec
def settings_get_value(setting_name: str):
    pass


@hs_hookspec
def settings_set_value(setting_name: str, setting_value):
    pass

from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


class SettingsStorage:
    @hs_hookspec
    def settings_get_value(self, setting_name: str):
        pass

    @hs_hookspec
    def settings_set_value(self, setting_name: str, setting_value):
        pass

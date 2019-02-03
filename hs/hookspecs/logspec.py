from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


class LogSpec:

    @hs_hookspec
    def log_trace(self, plugin_name, message):
        pass

    @hs_hookspec
    def log_debug(self, plugin_name, message):
        pass

    @hs_hookspec
    def log_notice(self, plugin_name, message):
        pass

    @hs_hookspec
    def log_warning(self, plugin_name, message):
        pass

    @hs_hookspec
    def log_exception(self, plugin_name, message):
        pass

    @hs_hookspec
    def log_error(self, plugin_name, message):
        pass

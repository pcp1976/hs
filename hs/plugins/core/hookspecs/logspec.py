from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


@hs_hookspec
def log_trace(plugin_name, message):
    pass


@hs_hookspec
def log_debug(plugin_name, message):
    pass


@hs_hookspec
def log_notice(plugin_name, message):
    pass


@hs_hookspec
def log_warning(plugin_name, message):
    pass


@hs_hookspec
def log_exception(plugin_name, message):
    pass


@hs_hookspec
def log_error(plugin_name, message):
    pass

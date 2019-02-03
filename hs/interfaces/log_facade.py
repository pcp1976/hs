import pluggy


class LogFacade:
    def __init__(self, pm: pluggy.PluginManager, plugin_name: str):
        self.pm = pm
        self.plugin_name = plugin_name
        self.func_map = {
            0: lambda message: self.pm.hook.log_trace(
                message=message, plugin_name=self.plugin_name
            ),
            1: lambda message: self.pm.hook.log_debug(
                message=message, plugin_name=self.plugin_name
            ),
            2: lambda message: self.pm.hook.log_notice(
                message=message, plugin_name=self.plugin_name
            ),
            3: lambda message: self.pm.hook.log_warning(
                message=message, plugin_name=self.plugin_name
            ),
            4: lambda message: self.pm.hook.log_exception(
                message=message, plugin_name=self.plugin_name
            ),
            5: lambda message: self.pm.hook.log_error(
                message=message, plugin_name=self.plugin_name
            ),
        }

    def trace(self, message):
        self.func_map[0](message)

    def debug(self, message):
        self.func_map[1](message)

    def notice(self, message):
        self.func_map[2](message)

    def warning(self, message):
        self.func_map[3](message)

    def exception(self, message):
        self.func_map[4](message)

    def error(self, message):
        self.func_map[5](message)

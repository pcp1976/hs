import pluggy


class LogFacade:
    def __init__(self, pm: pluggy.PluginManager, plugin_name: str):
        self.pm = pm
        self.plugin_name = plugin_name

    def _log(self, level, message):
        {
            0: lambda: self.pm.hook.log_trace(
                plugin_name=self.plugin_name, message=message
            ),
            1: lambda: self.pm.hook.log_debug(
                plugin_name=self.plugin_name, message=message
            ),
            2: lambda: self.pm.hook.log_notice(
                plugin_name=self.plugin_name, message=message
            ),
            3: lambda: self.pm.hook.log_warning(
                plugin_name=self.plugin_name, message=message
            ),
            4: lambda: self.pm.hook.log_exception(
                plugin_name=self.plugin_name, message=message
            ),
            5: lambda: self.pm.hook.log_error(
                plugin_name=self.plugin_name, message=message
            ),
        }[level]()

    def trace(self, message):
        self._log(0, message)

    def debug(self, message):
        self._log(1, message)

    def notice(self, message):
        self._log(2, message)

    def warning(self, message):
        self._log(3, message)

    def exception(self, message):
        self._log(4, message)

    def error(self, message):
        self._log(5, message)

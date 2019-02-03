from interfaces import HSPlugin
import os
from pluggy import HookimplMarker
from loguru import logger
import sys

log_impl = HookimplMarker("hs")

logger.remove()


class LogLoguru(HSPlugin):
    env_vars = os.environ

    def __init__(self):
        super().__init__()
        self.order = 3

    def activate(self):
        logger.add(
            sys.stderr,
            level=self.pm.hook.settings_get_value(
                setting_name="LOGGING_LEVEL"
            )[0],
            format="".join([
                "<c>{time}</c> ",
                "<level>|{level: <9}|</level> ",
                "<light-blue>{extra[plugin_name]: <20}</light-blue> ",
                "<white>{message}</white>"
            ])
        )
        self.log_notice("loguru logger", "activated")


    @log_impl
    def log_trace(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.trace(message)

    @log_impl
    def log_debug(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.debug(message)

    @log_impl
    def log_notice(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.info(message)

    @log_impl
    def log_warning(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.warning(message)

    @log_impl
    def log_exception(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.exception(message)

    @log_impl
    def log_error(self, plugin_name, message):
        logger_ctx = logger.bind(plugin_name=plugin_name)
        logger_ctx.error(message)

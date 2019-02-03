from yapsy.IPlugin import IPlugin
from pluggy import PluginManager
from .log_facade import LogFacade


class HSPlugin(IPlugin):
    name = None

    def __init__(self):
        super().__init__()
        self.pm: PluginManager = None
        self.order = 100
        self.log: LogFacade = None

    def link_pm(self, pm: PluginManager):
        pm.register(self)
        self.pm = pm
        self.log = LogFacade(pm, self.name)

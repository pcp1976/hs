from yapsy.IPlugin import IPlugin
from pluggy import PluginManager


class HSPlugin(IPlugin):
    def __init__(self):
        super().__init__()
        self.pm: PluginManager = None
        self.order = 100

    def link_pm(self, pm: PluginManager):
        pm.register(self)
        self.pm = pm

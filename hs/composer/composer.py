from yapsy.PluginManager import PluginManager
import os
from interfaces import HSPlugin
import pluggy


class Composer:
    drop_list = ["eventstore"]

    def __init__(self):
        self.plugin_places = [os.path.join(os.getcwd(), "plugins")]
        self.simple_plugin_manager = PluginManager()
        self.pm = pluggy.PluginManager("hs")
        self.plugin_info_list = None

    @staticmethod
    def plugin_order(element):
        plugin: HSPlugin = element.plugin_object
        return plugin.order

    def collect_plugins(self):
        self.simple_plugin_manager.setPluginPlaces(self.plugin_places)
        self.simple_plugin_manager.collectPlugins()
        self.plugin_info_list = self.simple_plugin_manager.getAllPlugins()
        self.plugin_info_list.sort(key=self.plugin_order)

    def activate_plugins(self):
        drop = []
        for pluginInfo in self.plugin_info_list:
            plugin: HSPlugin = pluginInfo.plugin_object
            plugin.link_pm(self.pm)
            # TODO: implement this in a settings file
            if plugin.name in self.drop_list:
                drop.append(pluginInfo)
                self.pm.unregister(plugin)
        for pluginInfo in self.plugin_info_list:
            if pluginInfo not in drop:
                plugin: HSPlugin = pluginInfo.plugin_object
                plugin.activate()

    def deactivate_plugins(self):
        for pluginInfo in self.plugin_info_list:
            plugin: HSPlugin = pluginInfo.plugin_object
            plugin.deactivate()

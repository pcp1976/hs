from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


class FilePaths:
    @hs_hookspec
    def filepath_get(self, plugin_name):
        """

        :param plugin_name: name of the plugin
        :return: string representing the path to that plugin's own subdirectory
        """
        pass

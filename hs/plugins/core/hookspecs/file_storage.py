from pluggy import HookspecMarker


hs_hookspec = HookspecMarker("hs")


@hs_hookspec
def file_store(filepath: str, storage_type: str) -> str:
    """
    :param filepath: path of the file to store
    :param storage_path: 'where' to put the file
    :param storage_type: to differentiate between different storage options
    :return: token to retrieve a file
    """
    pass


@hs_hookspec
def file_retrieve(filepath: str, token: str):
    """
    :param filepath: where to put the retrieved file
    :param token: token identifier for file
    """
    pass

@hs_hookspec
def artefact_storage_register(storage_type: str):
    """
    Relay all events to the artifact stream
    :param storage_type: name of the storage to register
    """
    pass


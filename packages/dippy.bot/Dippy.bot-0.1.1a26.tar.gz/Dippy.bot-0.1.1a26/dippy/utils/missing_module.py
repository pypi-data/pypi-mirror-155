class MissingModule:
    """Used in place of a module that couldn't be imported. If an attempt is made to access the module an import error
    will be raised."""

    def __init__(self, message: str):
        self.__message = message

    def __getattr__(self, item):
        raise ImportError(self.__message)

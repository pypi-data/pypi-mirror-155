class WorldAnvilClientException(Exception):
    """Base exception of the library."""


class NoParentCategoryException(WorldAnvilClientException):
    """When a category does not have a parent category this exception is thrown."""


class WorldAnvilServerException(WorldAnvilClientException):
    """Exceptions returned by the server for requests made."""


class ConnectionException(WorldAnvilClientException):
    """Was unable to connect to World Anvil for some reason."""


class UnexpectedStatusException(WorldAnvilServerException):
    """An unexpected status exception occurred."""

    def __init__(self, status: int, message: str, path: str):
        self.status = status
        self.message = message
        self.path = path


class InternalServerException(WorldAnvilServerException):
    """Internal Server Error in World Anvil Response."""

    def __init__(self, path: str):
        self.status = 500
        self.message = "Unable to process the request."
        self.path = path


class AccessForbidden(WorldAnvilServerException):
    """The user does not have permissions for the requested resources."""

    def __init__(self, path: str):
        self.status = 403
        self.message = "No permission to access the requested resource."
        self.path = path


class ResourceNotFound(WorldAnvilServerException):
    """The requested resource does not exist or was moved."""

    def __init__(self, path: str):
        self.status = 404
        self.message = "Request resource was not found."
        self.path = path

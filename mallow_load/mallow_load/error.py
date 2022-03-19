class Error(Exception):
    pass


class NotPresentInRepositoryError(Error):
    pass


class MappingDoesNotExistError(Error):
    pass

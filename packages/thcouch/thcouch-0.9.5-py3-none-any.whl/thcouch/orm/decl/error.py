__all__ = ['CouchLoaderError', 'FileConfigError']

from thresult import ResultException


class CouchLoaderError(ResultException):
    pass


class FileConfigError(CouchLoaderError):
    pass

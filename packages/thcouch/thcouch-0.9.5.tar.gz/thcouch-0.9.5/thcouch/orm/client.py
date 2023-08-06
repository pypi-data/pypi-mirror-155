__all__ = ['CouchClient']

import time
import asyncio

from typing import TypeAlias, Any

from thresult import Ok, Err, ResultException
from thcouch.core.server import GetServerOk, get_server
from ._error import CouchError
from .database import CouchDatabase


CouchClient: TypeAlias = 'CouchClient'


CouchClientResult: type = Ok[str] | Err[CouchError]


class CouchClient:
    uri: str

    
    def __init__(self, uri: str):
        self.uri = uri


    @CouchClientResult[CouchClient, Any]
    async def wait(self, timeout: float | None=None) -> CouchClient:
        '''
        This function awaits CouchDB to be ready/online.
        '''
        t = time.time()

        while True:
            server = (await get_server(uri=self.uri)).unwrap()
            if isinstance(server, GetServerOk):
                res = self
                break
            
            if timeout is not None:  # pragma: no cover
                dt = time.time() - t

                if dt > timeout:
                    e = CouchError('Timeout')
                    raise ResultException(e)

            await asyncio.sleep(1.0)  # pragma: no cover

        return res


    @CouchClientResult[CouchDatabase, Any]
    def database(self, db: str) -> CouchDatabase:
        '''
        This function creates instance of `CouchDatabase` type.
        This does not mean that database is created.
        '''
        database: CouchDatabase = CouchDatabase(self, db)

        if type(database) == CouchDatabase:
            return database

        raise ResultException(CouchError('Create CouchDatabase instance error'))  # pragma: no cover

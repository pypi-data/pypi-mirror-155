__all__ = ['CouchIndex']

from typing import Dict, Any, TypeAlias
from thcouch.core import index

from thresult import Ok, Err
from thcouch.core.index import IndexOk, post_index, GetIndexOk, get_index, DeleteIndexOk, delete_index
from ._error import CouchError


CouchIndex: TypeAlias = 'CouchIndex'
CouchDatabase: TypeAlias = 'CouchDatabase'


CouchIndexResult: type = Ok[CouchIndex] | Err[CouchError]


class CouchIndex():
    database: CouchDatabase
    name: str


    def __init__(self, database: CouchDatabase, name: str):
        self.database = database
        self.name = name


    @CouchIndexResult[CouchIndex, Any]
    async def create(self, doc: dict,
                     type: str='json',
                     ddoc: str | None=None,
                     name: str | None=None,
                     partial_filter_selector: dict | None=None,
                     partitioned: bool | None=None) -> CouchIndex:
        '''
        This function creates index into database.
        '''
        index_ok: IndexOk = (await post_index(uri=self.database.client.uri,
                                            db=self.database.db,
                                            index=doc,
                                            ddoc=ddoc,
                                            name=name,
                                            type=type,
                                            partial_filter_selector=partial_filter_selector,
                                            partitioned=partitioned)).unwrap()
    
        index_: GetIndexOk = (await get_index(uri=self.database.client.uri, db=self.database.db)).unwrap()
        indexes: list = index_.indexes[1:]  # skip default index on 0 position in list
            
        if len(indexes) == 0:  # pragma: no cover
            raise Exception('List of indexes is empty')
       
        for index_ in indexes:
            if index_['name'] == index_ok.name:
                couch_index: CouchIndex = CouchIndex(database=self.database, name=index_['name'])
                return couch_index
        else:
            raise Exception('Index was not created')  # pragma: no cover


    @CouchIndexResult[CouchIndex, Any]
    async def update(self, doc: dict,
                     type: str='json',
                     ddoc: str | None=None,
                     name: str | None=None,
                     partial_filter_selector: dict | None=None,
                     partitioned:  bool | None=None) -> CouchIndex:
        '''
        This function updates index from database.
        '''
        index_: IndexOk = (await post_index(uri=self.database.client.uri,
                                            db=self.database.db,
                                            index=doc,
                                            ddoc=ddoc,
                                            name=name,
                                            type=type,
                                            partial_filter_selector=partial_filter_selector,
                                            partitioned=partitioned)).unwrap()

        index_: GetIndexOk = (await get_index(uri=self.database.client.uri, db=self.database.db)).unwrap()
        indexes: list = index_.indexes[1:]  # skip default index on 0 position in list
        
        if len(indexes) == 0:  # pragma: no cover
            raise Exception('List of indexes is empty')
                 
        for index_ in indexes:
            if index_['name'] == name:
                couch_index: CouchIndex = CouchIndex(database=self.database, name=index_['name'])
                return couch_index
            else:
                raise Exception('Index was not updated: index cannot be found')  # pragma: no cover
        


    @CouchIndexResult[bool, Any]
    async def delete(self,
                     designdoc: str | None=None,
                     name: str | None=None) -> bool:
        '''
        This function deletes index from database
        '''
        index_: DeleteIndexOk = (await delete_index(uri=self.database.client.uri,
                                                    db=self.database.db,
                                                    designdoc=designdoc,
                                                    name=name)).unwrap()

        index_dict: dict = index_.__dict__
        
        res: bool = index_dict['ok']
        return res


    @CouchIndexResult[list[dict], Any]
    async def get(self) -> list[dict]:
        '''
        This function gets list of all indexes from database
        '''
        index_: GetIndexOk = (await get_index(uri=self.database.client.uri, db=self.database.db)).unwrap()
        indexes: list[dict] = index_.indexes[1:]  # skip default index on 0 position in list
        
        return indexes

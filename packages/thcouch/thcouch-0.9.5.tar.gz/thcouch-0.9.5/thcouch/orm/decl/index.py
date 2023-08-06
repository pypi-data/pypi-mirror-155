__all__ = ['BaseIndex']

from typing import Optional, TypeAlias, Any

from thresult import Result, Ok

from thcouch.orm.database import CouchDatabase
from thcouch.orm.index import CouchIndex


BaseIndex: TypeAlias = 'BaseIndex'
CouchLoader: TypeAlias = 'CouchLoader'


class BaseIndexType(type):
    def __repr__(cls) -> str:
        if hasattr(cls, 'fields'):
            pairs = ', '.join(f'{k}={v!r}' for k, v in cls.fields.items())
            return f'<class index {cls.__name__} {pairs}>'

        return f'<class index {cls.__name__} at {hex(id(cls))}>'


class BaseIndex(metaclass=BaseIndexType):
    id: str
    loader: CouchLoader
    name: str
    fields: list[str]
    type: str = 'json'


    def __init__(self, id, name, fields, type):
        self.id = id
        self.name = name
        self.fields = fields
        self.type = type


    @classmethod
    async def create(cls,
                     ddoc: Optional[str] = None,
                     partial_filter_selector: Optional[dict] = None,
                     partitioned: Optional[bool] = None) -> Result[BaseIndex, Any]:
        '''
        This method creates index
        '''
        db: CouchDatabase = cls.loader._db
        fields_dict = {'fields': cls.fields}
        couch_index = CouchIndex(db, cls.name)

        doc_index = (await couch_index.create(doc=fields_dict,
                                              name=cls.name,
                                              ddoc=ddoc,
                                              partial_filter_selector=partial_filter_selector,
                                              partitioned=partitioned)).unwrap()
        
        name: str = doc_index.name

        index_list: list = (await couch_index.get()).unwrap()

        for index in index_list:
            if index['name'] == name:
                return Ok(BaseIndex(id=index['ddoc'],
                                    name=index['name'],
                                    fields=index['def']['fields'],
                                    type=index['type']))
        else:
            raise Exception('Could not create index')  # pragma: no cover


    @classmethod
    async def delete(cls, designdoc: Optional[str] = None) -> Result[bool, Any]:
        '''
        This method deletes specified index from database, returns true if successful
        '''
        db: CouchDatabase = cls.loader._db
        couch_index = CouchIndex(db, cls.name)

        index_deleted: bool = (await couch_index.delete(designdoc=designdoc, name=cls.name)).unwrap()

        return Ok(index_deleted)


    @classmethod
    async def update(cls,
                     ddoc: Optional[str] = None,
                     partial_filter_selector: Optional[dict] = None,
                     partitioned: Optional[bool] = None) -> Result[BaseIndex, Any]:
        '''
        This method updates specified index from database, returns updated BaseIndex
        '''
        db: CouchDatabase = cls.loader._db
        fields_dict = {'fields': cls.fields}
        couch_index = CouchIndex(db, cls.name)

        doc_index = (await couch_index.update(doc=fields_dict,
                                              type=cls.type,
                                              name=cls.name,
                                              ddoc=ddoc,
                                              partial_filter_selector=partial_filter_selector,
                                              partitioned=partitioned)).unwrap()
        name = doc_index.name

        index_list: list = (await couch_index.get()).unwrap()

        for index in index_list:
            if index['name'] == name:
                return Ok(BaseIndex(id=index['ddoc'],
                                    name=index['name'],
                                    fields=index['def']['fields'],
                                    type=index['type']))
        else:
            raise Exception('Could not create index')  # pragma: no cover


    @classmethod
    async def get(cls) -> Result[list[BaseIndex], Any]:
        '''
        This method get list of all indexes from database, returns list of BaseIndexes
        '''
        db: CouchDatabase = cls.loader._db
        couch_index = CouchIndex(db, cls.name)

        index_list = (await couch_index.get()).unwrap()

        response_list = []
        for index in index_list:
            base_index = BaseIndex(id=index['ddoc'],
                                   name=index['name'],
                                   fields=index['def']['fields'],
                                   type=index['type'])
            response_list.append(base_index)

        return Ok(response_list)


__all__ = ['BaseModel']

from copy import deepcopy
from typing import Any, Union, TypeAlias, TypeVar

from thresult import Result, Ok, Err

from thcouch.orm.document import CouchDocument
from thcouch.orm.attachment import CouchAttachment

from .field import Field
from ..database import CouchDatabase


BaseModel: TypeAlias = 'BaseModel'
CouchLoader: TypeAlias = 'CouchLoader'


class BaseModelType(type):
    def __repr__(cls) -> str:
        if hasattr(cls, 'fields'):
            pairs = ', '.join(f'{k}={v!r}' for k, v in cls.fields.items())
            return f'<class model {cls.__name__} {pairs}>'

        return f'<class model {cls.__name__} at {hex(id(cls))}>'


    def __getitem__(cls, spec_type_params):
        if not isinstance(spec_type_params, tuple):
            spec_type_params = (spec_type_params,)

        # specialize types of generics
        type_params = dict(zip(cls.type_params, spec_type_params))
        new_ns = deepcopy(cls.ns) | type_params
        
        new_fields = {}
        
        for field_name, field in cls.fields.items():
            new_field: Field = eval(field.def_code, new_ns, cls.loader._ns)
            new_fields[field_name] = new_field

        new_ns: dict[str, Any] = deepcopy(cls.ns)
        new_type_name: str = f'{cls.__name__}{list(spec_type_params)}'
        new_type_bases: tuple[type] = (cls,)

        new_type_dict: dict = {
            'loader': cls.loader,
            'type_params': cls.type_params,
            'ns': new_ns,
            'fields': new_fields,
        }

        new_cls: type = type(new_type_name, new_type_bases, new_type_dict)
        return new_cls


    def __instancecheck__(cls, obj) -> bool:
        O: type = type(obj)
        
        if not issubclass(O, BaseModel):
            return False

        if cls is BaseModel:
            return True
        
        if not issubclass(O, cls.__bases__):
            return False # pragma: no cover

        # if hasattr(cls, 'type_params') and hasattr(O, 'type_params') and cls.type_params and O.type_params and cls.type_params != O.type_params:
        #     return False
        
        if hasattr(cls, 'type_params') and hasattr(O, 'type_params') and cls.type_params != O.type_params: # TODO: Check: and cls.type_params and O.type_params is unnecessary
            return False # pragma: no cover
        
        return True


class BaseModel(metaclass=BaseModelType):
    loader: CouchLoader         # class var
    type_params: list           # class var
    ns: dict[str, Any]          # class var
    fields: dict[str, Field]    # class var
    entries: dict[str, Any]


    def __init__(self, **kwargs):
        self.entries = {}

        for k, t in self.fields.items():
            if k in kwargs:
                v = kwargs[k]
            else:
                if callable(t.default):
                    v = t.default()
                else:
                    v = t.default

            def _deser(v: Any) -> Any:
                if isinstance(v, dict) and '$collection' in v:
                    entity_cls_name = v['$collection']
                    entity_type = self.loader._ns[entity_cls_name]
                    v = entity_type(**v)
                elif isinstance(v, list):
                    v = [_deser(n) for n in v]

                return v

            v = _deser(v)
            self.entries[k] = v

        self.validate().unwrap()


    def __repr__(self) -> str:
        pairs = ', '.join(f'{k}={v!r}' for k, v in self.entries.items())
        return f'<{self.__class__.__name__} Model {pairs}>'


    def __getitem__(self, key: str) -> Any:
        return self.entries[key]


    def __getattr__(self, attr: str) -> Any:
        return self.entries[attr]


    def __copy__(self) -> dict:
        return self.asdict()
    

    def __deepcopy__(self, memo: Any) -> dict:
        return self.asdict()


    def validate(self) -> Result[BaseModel, str]:
        for k, v in self.entries.items():
            t = self.fields[k]
            
            match obj := t.validate(v):
                case Err(e):
                    return Err[str](f'{k}: {e}')

        return Ok[BaseModel](self)


    def asdict(self) -> dict:
        return {
            '$collection': str(self.__class__.__name__),
            **deepcopy({
                k: v
                for k, v in self.entries.items()
                if self.fields[k].should_get(v)
            })
        }


    async def add(self) -> Result[BaseModel, Any]:
        '''
        This function adds the document to database
        '''
        db: CouchDatabase = self.loader._db
        doc: dict = self.asdict()
        model_type: BaseModelType = type(self) # self.__class__

        # add document dict
        res_tuple: tuple[CouchDatabase, CouchDocument] = (await db.add_document(doc=doc)).unwrap()

        # get document dict from res_tuple
        doc_: CouchDocument
        _, doc_ = res_tuple

        model_instance: BaseModel = model_type(**doc_)
        return Ok[BaseModel](model_instance)


    @classmethod
    async def get(cls, docid: str, rev: None | str=None) -> Result[BaseModel, Any]:
        '''
        This function gets the document from database by given docid and rev(latest)
        '''
        db: CouchDatabase = cls.loader._db
        model_type: BaseModelType = cls
        model_instance: BaseModel

        # get document dict
        doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()

        # instantiate model
        model_instance: BaseModel = model_type(**doc)
        return Ok(model_instance)
            
            
    @classmethod
    async def all(cls) -> Result[list[BaseModel], Any]:
        '''
        This function gets all documents from database
        '''
        db: CouchDatabase = cls.loader._db
        model_type: BaseModelType = cls

        # get all incomplete documents dicts
        incomplete_docs: list[CouchDocument] = (await db.all_docs()).unwrap()

        # create list of model instances
        model_instances: list[BaseModel] = []
        
        for incomplete_doc in incomplete_docs:
            docid = incomplete_doc['_id']
            rev = incomplete_doc['_rev']

            doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()

            # instantiate model
            model_instance: BaseModel = model_type(**doc)
            model_instances.append(model_instance)

        return Ok(model_instances)
    
            
    @classmethod
    async def bulk_get(cls,
                       docs: list[dict],
                       revs: None | bool = None) -> Result[list[BaseModel], Any]:
        '''
        This method can be called to query several documents in bulk.
        It is well suited for fetching a specific revision of documents,
        as replicators do for example, or for getting revision history
        '''
        db: CouchDatabase = cls.loader._db
        model_type: BaseModelType = cls
        documents: list[dict] = (await db.bulk_get(docs=docs, revs=revs)).unwrap()
        model_instances: list[BaseModel] = []

        for doc in documents:
            if 'ok' in doc['docs'][0]:
                doc_dict: dict = doc['docs'][0]['ok']

                # instantiate model
                model_instance: BaseModel = model_type(**doc_dict)
                model_instances.append(model_instance)
            else:
                model_instances.append(None)
            
        return Ok(model_instances)


    @classmethod
    async def bulk_docs(cls,
                        docs: list[Union[BaseModel, dict]],
                        new_edits: None | bool = None) -> Result[list[dict], Any]:
        '''
        This function allows you to create and update multiple documents at the same time within a single request
        '''
        if not docs:
            raise Exception('List of docs is empty')

        temp_docs: list[dict] = []
        
        for doc in docs:
            if isinstance(doc, BaseModel):
                temp_docs.append(doc.asdict())
            elif isinstance(doc, dict):
                temp_docs.append(doc)
            else:
                raise TypeError(f'Wrong element type! Expected "BaseModel" or "dict", received {type(doc)}')

        doc_tuple: tuple[CouchDatabase, list[dict]] = (await cls.loader._db.bulk_docs(docs=temp_docs, new_edits=new_edits)).unwrap()
        _, docs = doc_tuple
        res: list[dict] = docs
        return Ok(res)


    @classmethod
    async def find(cls,
                   selector: dict,
                   limit: None | int=None,
                   skip: None | int=None,
                   sort: None | list[dict | str]=None,
                   fields: None | list[str]=None,
                   use_index: None | (str | list[str])=None,
                   r: None | int=None,
                   bookmark: None | str=None,
                   update: None | bool=None,
                   stable: None | bool=None) -> Result[tuple[list[BaseModel], str, str], Any]:
        '''
        This function finds list of all documents by given selector(query)
        '''
        doc: tuple[list[dict], str, str] = (await cls.loader._db.find(selector=selector,
                                                                      limit=limit,
                                                                      skip=skip,
                                                                      sort=sort,
                                                                      fields=fields,
                                                                      use_index=use_index,
                                                                      r=r,
                                                                      bookmark=bookmark,
                                                                      update=update,
                                                                      stable=stable)).unwrap()

        docs, bookmark, warning = doc
        model_type: BaseModelType = cls
        models_list: list[BaseModel] = []
        
        for d in docs:
            model_instance: BaseModel = model_type(**d)
            models_list.append(model_instance)

        res = (models_list, bookmark, warning)
        return Ok(res)


    async def delete(self, batch: None | str=None) -> Result[BaseModel, Any]:
        '''
        This function deletes document from database
        '''
        db: CouchDatabase = self.loader._db
        model_type: BaseModelType = self.__class__
        model_instance: BaseModel
        # getting the document id and rev from instance of the document that's gonna be deleted
        docid: str = self.entries['_id']
        rev: None | str = self.entries.get('_rev')
        
        # get document obj
        doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()

        # delete document
        couch_doc_deleted: CouchDocument = (await doc.delete(batch=batch)).unwrap()
        
        self.entries['_deleted'] = True
        self.entries['rev'] = couch_doc_deleted['_rev']
            
        model_instance: BaseModel = model_type(**self.entries)
        return Ok(model_instance)


    async def update(self, doc: dict, batch: None | str=None, new_edits: None | bool=None) -> Result[BaseModel, Any]:
        '''
        This function updates/creates document from database
        '''
        db: CouchDatabase = self.loader._db
        id: str = self.entries['_id']
        rev: None | str = self.entries.get('_rev')
        model_type: BaseModelType = type(self)
        model_instance: BaseModel

        # get document obj
        couch_doc: CouchDocument = (await db.get_document(docid=id, rev=rev)).unwrap()
            
        # doc_update_dict: dict = couch_doc
        #
        # for key in doc.keys():
        #     if key in couch_doc.keys():
        #         couch_doc[key] = doc[key]
        #     elif key in self.fields.keys():
        #         couch_doc[key] = doc[key]
        #     else:
        #         raise KeyError(f'Could not update document: "{key}" doesn"t" exists')

        doc_update_dict: dict = couch_doc

        for key in doc.keys():
            if key in couch_doc.keys():
                doc_update_dict[key] = doc[key]
            elif key in self.fields.keys():
                doc_update_dict[key] = doc[key]
            else:
                raise KeyError(f'Could not update document: "{key}" doesn"t" exists')
        
        couch_doc_updated: CouchDocument = (await couch_doc.update(doc=doc_update_dict, rev=rev, batch=batch, new_edits=new_edits)).unwrap()
        model_instance = model_type(**couch_doc_updated)
        return Ok[BaseModel](model_instance)


    async def add_attachment(self, attachment_name: str, body: bytes) -> Result[tuple[BaseModel, CouchAttachment], Any]:
        '''
        This function adds attachment to the document from database
        '''
        db: CouchDatabase = self.loader._db
        id: str = self.entries['_id']
        rev: None | str = self.entries.get('_rev')
        couch_doc: CouchDocument
        model_type: BaseModelType = type(self)
        model_instance: BaseModel

        # get document obj
        couch_doc: CouchDocument = (await db.get_document(docid=id, rev=rev)).unwrap()
        # get data_tuple
        data_tuple: tuple[CouchDocument, CouchAttachment] = (await couch_doc.add_attachment(attachment_name=attachment_name, body=body)).unwrap()
        doc, att = data_tuple

        model_instance = model_type(**doc)
         
        resp_tuple: tuple[BaseModel, CouchAttachment] = (model_instance, att)
        return Ok(resp_tuple)


    async def get_attachment(self, attachment_name: str, range: str | None=None) -> Result[CouchAttachment, Any]:
        '''
        This function gets attachment from database
        '''
        db: CouchDatabase = self.loader._db
        docid: str = self.entries['_id']
        rev: str | None = self.entries.get('_rev')
        couch_doc: CouchDocument

        # get document obj
        couch_doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()

        # get document attachment
        attachment: CouchAttachment = (await couch_doc.get_attachment(docid=docid, attachment_name=attachment_name, rev=rev, range=range)).unwrap()
        return Ok(attachment)


    async def update_attachment(self, attachment_name: str, body: bytes) -> Result[tuple[BaseModel, CouchAttachment], Any]:
        '''
        This function updates attachment from database and returns tuple of documents and attachment
        '''
        db: CouchDatabase = self.loader._db
        docid: str = self.entries['_id']
        rev: None | str = self.entries.get('_rev')
        couch_doc: CouchDocument
        model_type: BaseModelType = type(self)
        model_instance: BaseModel

        couch_doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()
        data_tuple: tuple[CouchDocument, CouchAttachment] = (await couch_doc.add_attachment(attachment_name, body)).unwrap()
        doc, att = data_tuple

        # instanticate model
        model_instance = model_type(**doc)
        
        resp_tuple: tuple[BaseModel, CouchAttachment] = (model_instance, att)
        return Ok(resp_tuple)


    async def remove_attachment(self, attachment_name: str, batch: None | str=None) -> Result[BaseModel, Any]:
        '''
        This function removes attachment from database and returns the updated document without same attachment
        '''
        db: CouchDatabase = self.loader._db
        docid: str = self.entries['_id']
        rev: None | str = self.entries.get('_rev')
        model_type: BaseModelType = type(self)
        model_instance: BaseModel

        # get document obj
        doc: CouchDocument = (await db.get_document(docid=docid, rev=rev)).unwrap()
        model_dict: CouchDocument = (await doc.remove_attachment(attachment_name=attachment_name, batch=batch)).unwrap()

        # instantiate model
        model_instance = model_type(**model_dict)
        return Ok[BaseModel](model_instance)

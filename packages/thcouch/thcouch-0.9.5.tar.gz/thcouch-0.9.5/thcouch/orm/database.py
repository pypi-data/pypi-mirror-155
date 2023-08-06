__all__ = ['CouchDatabase']

from typing import TypeAlias, Any

from thresult import Ok, Err, ResultException
from thcouch.core.db import (
    head_db, put_db, post_db, delete_db, get_all_docs, bulk_get, bulk_docs, find_db,
    PostDbOk, GetAllDocsOk, BulkGetOk, FindDbOk,
)
from thcouch.core.doc import put_doc, get_doc, PutDocOk, GetDocOk
from thcouch.orm.index import CouchIndex
from thcouch.orm.document import CouchDocument
from ._error import CouchError
 
 
CouchDatabase: TypeAlias = 'CouchDatabase'
CouchClient: TypeAlias = 'CouchClient'


CouchDatabaseResult: type = Ok[str] | Err[CouchError]


class CouchDatabase:
    client: CouchClient
    db: str


    def __init__(self, client: CouchClient, db: str):
        self.client = client
        self.db = db


    @CouchDatabaseResult[CouchDatabase, Any]
    async def create(self, if_not_exists: bool=True) -> CouchDatabase:
        '''
        This function creates the database
        '''
        if (await head_db(uri=self.client.uri, db=self.db)).unwrap().exists:
            return self
        elif not if_not_exists:
            e = CouchError('Could not peek at database, server not responding')
            raise ResultException(e)

        await put_db(uri=self.client.uri, db=self.db)

        return self


    @CouchDatabaseResult[CouchDatabase, Any]
    async def delete(self) -> CouchDatabase:
        '''
        This function deletes the database
        '''
        await delete_db(uri=self.client.uri, db=self.db)

        return self


    @CouchDatabaseResult[tuple[CouchDatabase, CouchDocument], Any]
    async def add_document(self, doc: dict, batch: str | None = None) -> tuple[CouchDatabase, CouchDocument]:
        '''
        This function adds the document to the database
        '''
        id: None | str = None

        if '_id' in doc:
            id = doc['_id']

        resp: PutDocOk | PostDbOk = (await put_doc(uri=self.client.uri, db=self.db, docid=id, doc=doc)).unwrap() if id \
            else (await post_db(uri=self.client.uri, db=self.db, doc=doc, batch=batch)).unwrap()
        res_doc: dict = {**doc, '_id': resp.id, '_rev': resp.rev}

        if res_doc is None:  # pragma: no cover
            e = CouchError(f'Could not insert document {doc!r}')
            raise ResultException(e)

        document: CouchDocument = CouchDocument(self, **res_doc)
        res: tuple[CouchDatabase, CouchDocument] = (self, document)

        return res


    add = add_document


    @CouchDatabaseResult[CouchDocument, Any]
    async def get_document(self,
                           docid: str,
                           attachments: bool | None=None,
                           att_encoding_info: bool | None=None,
                           atts_since: list | None=None,
                           conflicts: bool | None=None,
                           deleted_conflicts: bool | None=None,
                           latest: bool | None=None,
                           local_seq: bool | None=None,
                           meta: bool | None=None,
                           open_revs: list | None=None,
                           rev: str | None=None,
                           revs: bool | None=None,
                           revs_info: bool | None=None) -> CouchDocument:
        '''
        This function gets the specific document from the database by given docid and/or rev(latest)
        '''
        get_doc_: GetDocOk = (await get_doc(uri=self.client.uri,
                                            db=self.db,
                                            docid=docid,
                                            attachments=attachments,
                                            att_encoding_info=att_encoding_info,
                                            atts_since=atts_since,
                                            conflicts=conflicts,
                                            deleted_conflicts=deleted_conflicts,
                                            latest=latest,
                                            local_seq=local_seq,
                                            meta=meta,
                                            open_revs=open_revs,
                                            rev=rev,
                                            revs=revs,
                                            revs_info=revs_info)).unwrap()

        doc_dict: dict = get_doc_.doc
        document = CouchDocument(self, **doc_dict)

        return document


    get = get_document


    @CouchDatabaseResult[list[CouchDocument], Any]
    async def all_docs(self) -> list[CouchDocument]:
        '''
        This function gets list of all documents from the database
        '''
        get_all_docs_: GetAllDocsOk = (await get_all_docs(uri=self.client.uri, db=self.db)).unwrap()
        rows: list[dict] = get_all_docs_.rows

        documents = []
        for r in rows:
            doc_id: str = r['id']
            doc_rev: str = r['value']['rev']

            get_doc_ = (await self.get_document(docid=doc_id, rev=doc_rev)).unwrap()
            documents.append(get_doc_)

        return documents


    all = all_docs


    @CouchDatabaseResult[list[dict], Any]
    async def bulk_get(self, docs: list[dict], revs: bool | None=None) -> list[dict]:
        '''
        This function gets bulk documents from database
        '''
        bulk_get_: BulkGetOk = (await bulk_get(uri=self.client.uri, db=self.db, docs=docs, revs=revs)).unwrap()
        res: list[dict] = bulk_get_.results

        return res


    @CouchDatabaseResult[tuple[CouchDatabase, list[dict]], Any]
    async def bulk_docs(self, docs: list[dict], new_edits: bool | None=None) -> tuple[CouchDatabase, list[dict]]:
        '''
        This function creates or updates multiple documents at the same time within a single request
        https://docs.couchdb.org/en/stable/replication/protocol.html?highlight=2.4.2.5.2#upload-batch-of-changed-documents
        https://github.com/apache/couchdb-documentation/issues/390
        '''
        bulk_docs_ = (await bulk_docs(uri=self.client.uri, db=self.db, docs=docs, new_edits=new_edits)).unwrap()
        documents: list[dict] = bulk_docs_.results
        res: tuple[CouchDatabase, list[dict]] = (self, documents)

        return res


    @CouchDatabaseResult[tuple[list[dict], str, str], Any]
    async def find(self,
                   selector: dict,
                   limit: int | None=None,
                   skip: int | None=None,
                   sort: list[dict | str] | None=None,
                   fields: list[str] | None=None,
                   use_index: (str | list[str]) | None=None,
                   r: int | None=None,
                   bookmark: str | None=None,
                   update: bool | None=None,
                   stable: bool | None=None) -> tuple[list[dict], str, str]:
        '''
        This function finds list of all documents by given selector(query)
        '''
        find_db_: FindDbOk = (await find_db(uri=self.client.uri,
                                            db=self.db,
                                            selector=selector,
                                            limit=limit,
                                            skip=skip,
                                            sort=sort,
                                            fields=fields,
                                            use_index=use_index,
                                            r=r,
                                            bookmark=bookmark,
                                            update=update,
                                            stable=stable)).unwrap()

        docs: list[dict] = find_db_.docs
        bookmark: str = find_db_.bookmark
        warning: str = find_db_.warning
        res: tuple[list[dict], str, str] = (docs, bookmark, warning)

        return res


    def index(self, name: str) -> CouchIndex:
        '''
        This function creates the instance of CouchIndex
        '''
        index: CouchIndex = CouchIndex(database=self, name=name)

        return index

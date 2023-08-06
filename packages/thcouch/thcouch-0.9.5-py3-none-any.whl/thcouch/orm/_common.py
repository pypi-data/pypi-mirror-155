__all__ = ['CouchDocument', 'CouchDocumentResult', 'CouchAttachment', 'CouchAttachmentResult']

from typing import Dict, Any, TypeAlias

from thresult import Ok, Err
from thcouch.core.doc import get_doc, GetDocOk, PutDocOk, put_doc, DeleteDocOk, delete_doc
from thcouch.core.attachment import (
    DeleteAttachmentOk, delete_attachment,
    GetAttachmentOk, get_attachment,
    PutAttachmentOk, put_attachment,
)


CouchDocument: TypeAlias = 'CouchDocument'
CouchAttachment: TypeAlias = 'CouchAttachment'
CouchDatabase: TypeAlias = 'CouchDatabase'


CouchDocumentResult: type = Ok[str] | Err[Any]


class CouchDocument(Dict[str, Any]):
    database: CouchDatabase
    _id: str
    _rev: str
    _deleted: None | bool


    def __init__(self, database: CouchDatabase, **doc):
        self.database = database
        super().update(doc)


    @CouchDocumentResult[CouchDocument, Any]
    async def update(self,
                     doc: dict,
                     rev: str | None=None,
                     batch: str | None=None,
                     new_edits: bool | None=None) -> CouchDocument:
        '''
        This function updates the document from database
        '''
        doc_put: PutDocOk = (await put_doc(uri=self.database.client.uri,
                                           db=self.database.db,
                                           docid=self['_id'],
                                           doc=doc,
                                           rev=rev,
                                           batch=batch,
                                           new_edits=new_edits)).unwrap()

        res_doc: dict = {**doc, '_id': doc_put.id, '_rev': doc_put.rev}

        document = CouchDocument(self.database, **res_doc)
        return document


    @CouchDocumentResult[CouchDocument, Any]
    async def delete(self, batch: str | None=None) -> CouchDocument:
        '''
        This function deletes the document from database
        '''
        id: str = self['_id']
        rev: str = self['_rev']

        doc_deleted: DeleteDocOk = (await delete_doc(self.database.client.uri,
                                                     db=self.database.db,
                                                     docid=id,
                                                     rev=rev,
                                                     batch=batch)).unwrap()

        res_doc = {'_id': doc_deleted.id, '_rev': doc_deleted.rev, '_deleted': doc_deleted.ok}
        document = CouchDocument(self.database, **res_doc)

        return document


    @CouchDocumentResult[tuple[CouchDocument, CouchAttachment], Any]
    async def add_attachment(self, attachment_name: str, body: bytes) -> tuple[CouchDocument, CouchAttachment]:
        '''
        This function adds the attachment to specific document from database
        '''
        id: str = self['_id']
        rev: str = self['_rev']

        put_att: PutAttachmentOk = (await put_attachment(self.database.client.uri,
                                                         db=self.database.db,
                                                         docid=id,
                                                         attachment_name=attachment_name,
                                                         rev=rev,
                                                         body=body)).unwrap()
        # get newly updated document
        doc: CouchDocument = (await self.database.get_document(docid=id)).unwrap()

        # attachment
        doc_attachments: dict = doc['_attachments']
        attachment_dict: dict = doc_attachments[attachment_name]
        att_dict = {}
        att_dict['attachment_name']=attachment_name
        att_dict['digest']=attachment_dict['digest']
        att_dict['length']=attachment_dict['length']
        att_dict['revpos']=attachment_dict['revpos']
        att_dict['stub']=attachment_dict['stub']
        attachment = CouchAttachment(self, **att_dict)

        res = (doc, attachment)
        return res


    @CouchDocumentResult[CouchAttachment, Any]
    async def get_attachment(self,
                             docid: str,
                             attachment_name: str,
                             rev: str | None=None,
                             range: None | str=None) -> CouchAttachment:
        '''
        This function gets the attachment from specific document from database
        '''
        att: GetAttachmentOk = (await get_attachment(uri=self.database.client.uri,
                                                     db=self.database.db,
                                                     docid=docid,
                                                     attname=attachment_name)).unwrap()

        doc: CouchDocument = (await self.database.get_document(docid=docid, rev=rev)).unwrap()

        # document
        document: CouchDocument = CouchDocument(self.database, **doc)

        # attachment
        doc_attachments: dict = doc['_attachments']
        attachment_dict: dict = doc_attachments[attachment_name]

        # attachment
        att_dict = {}
        att_dict['attachment_name']=attachment_name
        att_dict['digest']=attachment_dict['digest']
        att_dict['length']=attachment_dict['length']
        att_dict['revpos']=attachment_dict['revpos']
        att_dict['stub']=attachment_dict['stub']

        attachment = CouchAttachment(self, **att_dict)

        return attachment


    @CouchDocumentResult[CouchDocument, Any]
    async def remove_attachment(self,
                                attachment_name: str,
                                batch: str | None=None) -> CouchDocument:
        '''
        This function remove the attachment from specific document from database
        '''
        att: DeleteAttachmentOk = (await delete_attachment(uri=self.database.client.uri,
                                                           db=self.database.db,
                                                           docid=self['_id'],
                                                           attname=attachment_name,
                                                           rev=self['_rev'],
                                                           batch=batch)).unwrap()

        doc: CouchDocument = (await self.database.get_document(docid=att.id, rev=att.rev)).unwrap()
        document = CouchDocument(self.database, **doc)

        return document



CouchAttachmentResult: type = Ok[CouchAttachment] | Err[Any]


class CouchAttachment(Dict[str, Any]):
    document: CouchDocument
    attachment_name: str
    digest: str
    length: int
    revpos: int
    stub: bool


    def __init__(self, document: CouchDocument, **att):
        self.document = document
        super().update(att)


    @CouchAttachmentResult[CouchAttachment, Any]
    async def get(self, docid: str,
                  attname: str,
                  rev: str | None=None,
                  range: str | None=None) -> CouchAttachment:
        '''
        This function gets the attachment from database by given id, attachment name and/or rev
        '''
        # 1. Gets the attachment by given id
        attachment_: GetAttachmentOk = (await get_attachment(uri=self.document.database.client.uri,
                                                             db=self.document.database.db,
                                                             docid=docid,
                                                             attname=attname,
                                                             rev=rev,
                                                             range=range)).unwrap()

        # 2. Gets the document by given id
        document_: GetDocOk = (await get_doc(uri=self.document.database.client.uri,
                                             db=self.document.database.db,
                                             docid=docid)).unwrap()

        document_ = document_.__dict__['doc']

        attachments = document_['_attachments']
        attachments = attachments[attname]

        digest = attachments['digest']
        length = attachments['length']
        revpos = attachments['revpos']
        stub = attachments['stub']

        couch_document = CouchDocument(database=self.document.database,
                                       _id=document_['_id'],
                                       _rev=document_['_rev'],
                                       doc=document_)

        couch_attachment: CouchAttachment = CouchAttachment(attachment_name=attname,
                                                            document=couch_document,
                                                            digest=digest,
                                                            length=length,
                                                            revpos=revpos,
                                                            stub=stub,
                                                            att=attachment_.__dict__)

        return couch_attachment


    @CouchAttachmentResult[tuple[CouchDocument, CouchAttachment], Any]
    async def update(self,
                     docid: str,
                     attachment_name: str,
                     body: bytes,
                     rev: str | None = None) -> tuple[CouchDocument, CouchAttachment]:
        '''
        This function updates the attachment from database by given id and attachment name
        '''

        # 1. update/or create attachment
        attachment_put: PutAttachmentOk = (await put_attachment(uri=self.document.database.client.uri,
                                                                db=self.document.database.db,
                                                                docid=docid,
                                                                attachment_name=attachment_name,
                                                                rev=rev,
                                                                body=body)).unwrap()

        # 2. Gets the updated/created attachment
        attachment_get: GetAttachmentOk = (await get_attachment(uri=self.document.database.client.uri,
                                                                db=self.document.database.db,
                                                                docid=attachment_put.id,
                                                                attname=attachment_name,
                                                                rev=attachment_put.rev)).unwrap()

        # 3. Gets the updated document
        document_: GetDocOk = (await get_doc(uri=self.document.database.client.uri,
                                             db=self.document.database.db,
                                             docid=docid)).unwrap()

        document_ = document_.__dict__['doc']

        attachments = document_['_attachments']
        attachments = attachments[attachment_name]

        digest = attachments['digest']
        length = attachments['length']
        revpos = attachments['revpos']
        stub = attachments['stub']

        couch_document = CouchDocument(database=self.document.database,
                                       _id=document_['_id'],
                                       _rev=document_['_rev'],
                                       doc=document_)

        couch_attachment: CouchAttachment = CouchAttachment(attachment_name=attachment_name,
                                                            document=couch_document,
                                                            digest=digest,
                                                            length=length,
                                                            revpos=revpos,
                                                            stub=stub,
                                                            att=attachment_get.__dict__)
        
        res = (couch_document, couch_attachment)
        return res


    @CouchAttachmentResult[tuple[CouchDocument, CouchAttachment], Any]
    async def remove(self,
                     docid: str,
                     attname: str,
                     rev: str=None,
                     batch: str | None=None) -> tuple[CouchDocument, CouchAttachment]:
        '''
        This function removes the attachment from database by given docid, attachment name and/or rev
        '''

        # 1. remove att
        atachment_deleted: DeleteAttachmentOk = (await delete_attachment(uri=self.document.database.client.uri,
                                                                         db=self.document.database.db,
                                                                         docid=docid,
                                                                         attname=attname,
                                                                         rev=rev,
                                                                         batch=batch)).unwrap()

        # 2. get doc
        document_: GetDocOk = (await get_doc(uri=self.document.database.client.uri,
                                             db=self.document.database.db,
                                             docid=docid)).unwrap()

        document_ = document_.__dict__['doc']

        couch_document = CouchDocument(database=self.document.database,
                                       _id=document_['_id'],
                                       _rev=document_['_rev'],
                                       doc=document_)
        # 3. return (doc, attn)
        res: tuple[CouchDocument, CouchAttachment] = (couch_document, self)

        return res

'''
Reference:
   https://docs.couchdb.org/en/stable/api/document/attachments.html#delete--db-docid-attname
'''
__all__ = ['DeleteAttachmentResult', 'DeleteAttachmentOk', 'DeleteAttachmentErr', 'delete_attachment']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class DeleteAttachmentOk:
    id: str
    ok: bool
    rev: str


@dataclass
class DeleteAttachmentErr:
    error: str
    reason: str


DeleteAttachmentResult: type = Ok[DeleteAttachmentOk] | Err[DeleteAttachmentErr]


@DeleteAttachmentResult[DeleteAttachmentOk, DeleteAttachmentErr]
async def delete_attachment(uri: str,
                            db: str,
                            docid: str,
                            attname: str,
                            rev: str = None,
                            batch: str | None=None) -> DeleteAttachmentOk:
    '''
    This function deletes the attachment from database by given docid
    '''
    url: str = f'{uri}/{db}/{docid}/{attname}'
    params = {}
    
    if rev is not None:
        params['rev'] = rev
    
    if batch is not None:
        params['batch'] = batch

    async with ClientSession() as session:
        try:
            async with session.delete(url, params=params) as resp:
                data = await resp.json()
                if resp.status in (200, 202):
                    res = DeleteAttachmentOk(**data)
                elif resp.status == 400:
                    res = DeleteAttachmentErr('Bad Request', 'Invalid request body or parameters')
                elif resp.status == 401:
                    res = DeleteAttachmentErr('Unauthorized', 'Write privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = DeleteAttachmentErr('Not Found', 'Specified database, document or attachment was not found')
                elif resp.status == 409:
                    res = DeleteAttachmentErr('Conflict', 'Document’s revision wasn’t specified or it’s not the latest')
                else:
                    res = DeleteAttachmentErr('Unknown Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = DeleteAttachmentErr('Exception', e)

    if isinstance(res, DeleteAttachmentErr):
        raise ResultException(res)

    return res

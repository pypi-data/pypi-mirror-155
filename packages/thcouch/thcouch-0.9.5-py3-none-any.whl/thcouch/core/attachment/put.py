'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/attachments.html#put--db-docid-attname
'''
__all__ = ['PutAttachmentResult', 'PutAttachmentOk', 'PutAttachmentErr', 'put_attachment']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class PutAttachmentOk:
    id: str
    ok: bool
    rev: str


@dataclass
class PutAttachmentErr:
    error: str
    reason: str


PutAttachmentResult: type = Ok[PutAttachmentOk] | Err[PutAttachmentErr]


@PutAttachmentResult[PutAttachmentOk, PutAttachmentErr]
async def put_attachment(uri: str,
                         db: str,
                         docid: str,
                         attachment_name: str,
                         rev: str,
                         body: bytes) -> PutAttachmentOk:
    '''
    This function creates/updates the attachment by given docid, attachment name, rev (latest) and body 
    '''
    url: str = f'{uri}/{db}/{docid}/{attachment_name}'    
    params = {}
    params['rev'] = rev

    async with ClientSession() as session:
        try:
            async with session.put(url, params=params, data=body) as resp:
                data = await resp.json()

                if resp.status in (201, 202):
                    res = PutAttachmentOk(**data)
                elif resp.status == 400:
                    res = PutAttachmentErr('Bad Request', 'Invalid request body or parameters')
                elif resp.status == 401:
                    res = PutAttachmentErr('Unauthorized', 'Write privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = PutAttachmentErr('Not Found', 'Specified database, document or attachment was not found')
                elif resp.status == 409:
                    res = PutAttachmentErr('Conflict', 'Document’s revision wasn’t specified or it’s not the latest')
                else:
                    res = PutAttachmentErr('Unknown Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = PutAttachmentErr('Exception', e)

    if isinstance(res, PutAttachmentErr):
        raise ResultException(res)

    return res

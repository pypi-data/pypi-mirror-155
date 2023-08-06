'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/attachments.html#head--db-docid-attname
'''
__all__ = ['HeadAttachmentResult', 'HeadAttachmentOk', 'HeadAttachmentErr', 'head_attachment']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class HeadAttachmentOk:
    pass


@dataclass
class HeadAttachmentErr:
    error: str
    reason: str


HeadAttachmentResult: type = Ok[HeadAttachmentOk] | Err[HeadAttachmentErr]


@HeadAttachmentResult[HeadAttachmentOk, HeadAttachmentErr]
async def head_attachment(uri: str, db: str, docid: str, attname: str, rev: str | None=None) -> HeadAttachmentOk:
    '''
    This function gets head of attachment from database by given docid and attachment name
    '''
    url: str = f'{uri}/{db}/{docid}/{attname}'
    params = {}
    
    if rev is not None:
        params['rev'] = rev

    async with ClientSession() as session:
        try:
            async with session.head(url, params=params) as resp:
                if resp.status == 200:
                    res = HeadAttachmentOk()
                elif resp.status == 401:
                    res = HeadAttachmentErr('Unauthorized', 'Read privilege required')  # pragma: no cover
                elif resp.status == 404:
                    res = HeadAttachmentErr('Not Found', 'Specified database, document or attachment was not found')
                else:
                    res = HeadAttachmentErr('Unknown Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = HeadAttachmentErr('Exception', e)

    if isinstance(res, HeadAttachmentErr):
        raise ResultException(res)

    return res

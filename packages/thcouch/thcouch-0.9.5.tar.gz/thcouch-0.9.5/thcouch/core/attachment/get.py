'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
'''
__all__ = ['GetAttachmentResult', 'GetAttachmentOk', 'GetAttachmentErr', 'get_attachment']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetAttachmentOk:
    accept_ranges: bool | None
    content_type: str | None
    content_encoding: str | None
    content_length: str | None
    etag: str | None
    body: bytes


@dataclass
class GetAttachmentErr:
    error: str
    reason: str


GetAttachmentResult: type = Ok[GetAttachmentOk] | Err[GetAttachmentErr]


@GetAttachmentResult[GetAttachmentOk, GetAttachmentErr]
async def get_attachment(uri: str,
                         db: str,
                         docid: str,
                         attname: str,
                         rev: str | None=None,
                         range: str | None=None) -> GetAttachmentOk:
    '''
    This function gets the attachment from database by given docid and attachemnt name
    '''
    
    url: str = f'{uri}/{db}/{docid}/{attname}'
    params = {}
    
    if rev is not None:
        params['rev'] = rev
    
    headers = {}

    if range is not None:
        headers = {**headers, 'Range': range}

    async with ClientSession() as session:
        try:
            async with session.get(url, params=params, headers=headers) as resp:
                resp_body: bytes = await resp.read()

                if resp.status == 200:
                    data: dict = {
                        'accept_ranges': resp.headers.get('Accept-Ranges', None),
                        'content_type': resp.headers.get('Content-Type', None),
                        'content_encoding': resp.headers.get('Content-Encoding', None),
                        'content_length': resp.headers.get('Content-Length', None),
                        'etag': resp.headers.get('ETag', None),
                        'body': resp_body,
                    }

                    res = GetAttachmentOk(**data)
                elif resp.status == 401:
                    res = GetAttachmentErr('Unauthorized', 'Read privilege required')  # pragma: no cover
                elif resp.status == 404:
                    res = GetAttachmentErr('Not Found', 'Specified database, document or attachment was not found')
                else:
                    res = GetAttachmentErr('Unknown Error', f'Unknown Status Error: {resp.status}')
        except Exception as e:
            res = GetAttachmentErr('Exception', e)

    if isinstance(res, GetAttachmentErr):
        raise ResultException(res)

    return res


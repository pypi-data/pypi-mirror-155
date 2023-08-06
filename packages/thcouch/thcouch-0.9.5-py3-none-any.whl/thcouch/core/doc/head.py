'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/common.html#head--db-docid
'''
__all__ = ['HeadDocResult', 'HeadDocOk', 'HeadDocErr', 'head_doc']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class HeadDocOk:
    pass


@dataclass
class HeadDocErr:
    error: str
    reason: str


HeadDocResult: type = Ok[HeadDocOk] | Err[HeadDocErr]


@HeadDocResult[HeadDocOk, HeadDocErr]
async def head_doc(uri: str, db: str, docid: str) -> HeadDocOk:
    '''
    This function returns the HTTP Headers containing a minimal amount of information about the specified document
    '''
    url: str = f'{uri}/{db}/{docid}'

    async with ClientSession() as session:        
        try:
            async with session.head(url) as resp:
                if resp.status in (200, 304):
                    res = HeadDocOk()
                elif resp.status == 401:
                    res = HeadDocErr('Unauthorized', 'Read privilege required')  # pragma: no cover
                elif resp.status == 404:
                    res = HeadDocErr('Not Found', 'Document not found')
                else:
                    res = HeadDocErr('Unknown error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = HeadDocErr('Exception', e)

    if isinstance(res, HeadDocErr):
        raise ResultException(res)

    return res

'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_all_docs
'''
__all__ = ['GetAllDocsResult', 'GetAllDocsOk', 'GetAllDocsErr', 'get_all_docs']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetAllDocsOk:
    total_rows: int
    offset: int
    rows: list[dict]


@dataclass
class GetAllDocsErr:
    error: str
    reason: str


GetAllDocsResult: type = Ok[GetAllDocsOk] | Err[GetAllDocsErr]


@GetAllDocsResult[GetAllDocsOk, GetAllDocsErr]
async def get_all_docs(uri: str, db: str) -> GetAllDocsOk:
    '''
    This function gets all documents from database
    '''
    url: str = f'{uri}/{db}/_all_docs'

    async with ClientSession() as session:        
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = GetAllDocsOk(**data)
                elif resp.status == 404:
                    res = GetAllDocsErr('Not Found', 'Requested database not found')
                else:
                    res = GetAllDocsErr('Status Error',f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = GetAllDocsErr('Exception', e)
            
    if isinstance(res, GetAllDocsErr):
        raise ResultException(res)

    return res
    
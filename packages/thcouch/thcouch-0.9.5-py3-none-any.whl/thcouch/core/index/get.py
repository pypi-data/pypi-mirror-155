'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/find.html#get--db-_index
'''
__all__ = ['GetIndexResult', 'GetIndexOk', 'GetIndexErr', 'get_index']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetIndexOk:
    total_rows: int
    indexes: list[dict]


@dataclass
class GetIndexErr:
    error: str
    reason: str


GetIndexResult: type = Ok[GetIndexOk] | Err[GetIndexErr]


@GetIndexResult[GetIndexOk, GetIndexErr]
async def get_index(uri: str, db: str) -> GetIndexOk: 
    '''
    This function gets the list of Indexes from database
    '''
    url: str = f'{uri}/{db}/_index'
    
    async with ClientSession() as session:
        try:
            async with session.get(url) as resp:
                data: dict = await resp.json()
                
                if resp.status == 200:
                    res = GetIndexOk(**data)
                elif resp.status == 400:
                    res = GetIndexErr('Bad Request', 'Invalid request')  # pragma: no cover
                elif resp.status == 401:  # pragma: no cover
                    res = GetIndexErr('Unauthorized', 'Read permission required')
                elif resp.status == 404:
                    res = GetIndexErr('Bad Request', 'Not Found')
                elif resp.status == 500:  # pragma: no cover
                    res = GetIndexErr('Internal Server Error', 'Query execution error')
                else:
                    res = GetIndexErr('Unknown Error', f'Unrecognized CouchDB status: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = GetIndexErr('Exception', e)

    if isinstance(res, GetIndexErr):
        raise ResultException(res)
    
    return res

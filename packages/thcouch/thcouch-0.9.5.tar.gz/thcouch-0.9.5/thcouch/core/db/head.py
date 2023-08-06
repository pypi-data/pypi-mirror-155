'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/common.html#head--db
'''
__all__ = ['HeadDbResult', 'HeadDbOk', 'HeadDbErr', 'head_db']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class HeadDbOk:
    exists: bool


@dataclass
class HeadDbErr:
    error: str
    reason: str


HeadDbResult: type = Ok[HeadDbOk] | Err[HeadDbErr]


@HeadDbResult['HeadDbOk', 'HeadDbErr']
async def head_db(uri: str, db: str) -> HeadDbOk:
    '''
    This function returns the HTTP Headers containing a minimal amount
    of information about the specified database. Since the response body is empty,
    using the HEAD method is a lightweight way to check if the database exists already or not
    '''
    
    url: str = f'{uri}/{db}'

    async with ClientSession() as session:        
        try:
            async with session.head(url) as resp:
                if resp.status == 200:
                    res = HeadDbOk(True)
                elif resp.status == 404:
                    res = HeadDbOk(False)
                else:
                    res = HeadDbErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:  # pragma: no cover
            res = HeadDbErr('Exception', e)

    if isinstance(res, HeadDbErr):
        raise ResultException(res) 

    return res
 
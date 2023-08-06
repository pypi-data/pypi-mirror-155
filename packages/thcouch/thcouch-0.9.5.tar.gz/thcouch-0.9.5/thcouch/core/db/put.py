'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/common.html#put--db
'''
__all__ = ['PutDbResult', 'PutDbOk', 'PutDbErr', 'put_db']

import json

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class PutDbOk:
    ok: bool


@dataclass
class PutDbErr:
    error: str
    reason: str


PutDbResult: type = Ok[PutDbOk] | Err[PutDbErr]


@PutDbResult[PutDbOk, PutDbErr]
async def put_db(uri: str, db: str, q: int=8, n: int=3, partitioned: bool=False) -> PutDbOk:
    '''
    This function creates/updates the database
    '''
    url: str = f'{uri}/{db}'
    
    params = {
        'q': q,
        'n': n,
        'partitioned': json.dumps(partitioned),
    }

    async with ClientSession() as session:
        try:
            async with session.put(url, params=params) as resp:
                if resp.status in (201, 202):
                    data = await resp.json()
                    res = PutDbOk(**data)
                elif resp.status == 400:
                    res = PutDbErr('Bad Request', 'Invalid database name')
                elif resp.status == 401:
                    res = PutDbErr('Unauthorized',
                                   'CouchDB Server Administrator privileges required')  # pragma: no cover
                elif resp.status == 412:
                    res = PutDbErr('Precondition Failed', 'Database already exists')
                else:
                    res = PutDbErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = PutDbErr('Exception', e)

    if isinstance(res, PutDbErr):
        raise ResultException(res)

    return res

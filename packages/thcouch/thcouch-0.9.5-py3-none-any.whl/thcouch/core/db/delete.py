'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/common.html#delete--db
'''
__all__ = ['DeleteDbResult', 'DeleteDbOk', 'DeleteDbErr', 'delete_db']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class DeleteDbOk:
    ok: bool

@dataclass
class DeleteDbErr:
    error: str
    reason: str


DeleteDbResult: type = Ok[DeleteDbOk] | Err[DeleteDbErr]


@DeleteDbResult[DeleteDbOk, DeleteDbErr]
async def delete_db(uri: str, db: str) -> DeleteDbOk:
    '''
    This function deletes the db
    '''

    url: str = f'{uri}/{db}'

    async with ClientSession() as session:        
        try:
            async with session.delete(url) as resp:
                if resp.status in (200, 202):
                    data = await resp.json()
                    res = DeleteDbOk(**data)
                elif resp.status == 400:
                    res = DeleteDbErr('Bad Request', 'Invalid database name or forgotten document id by accident')  # pragma: no cover
                elif resp.status == 401:
                    res = DeleteDbErr('Unauthorized', 'CouchDB Server Administrator privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = DeleteDbErr('Not Found', 'Database doesn’t exist or invalid database name')
                else:
                    res = DeleteDbErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = DeleteDbErr('Exception', e)

    if isinstance(res, DeleteDbErr):
        raise ResultException(res)

    return res

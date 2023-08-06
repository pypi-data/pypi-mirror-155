'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/common.html#post--db
'''
__all__ = ['PostDbResult', 'PostDbOk', 'PostDbErr', 'post_db']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class PostDbOk:
    id: str
    ok: bool
    rev: str


@dataclass
class PostDbErr:
    error: str
    reason: str


PostDbResult: type = Ok[PostDbOk] | Err[PostDbErr]


@PostDbResult[PostDbOk, PostDbErr]
async def post_db(uri: str, db: str, doc: dict, batch: str | None=None) -> PostDbOk:
    '''
    This function creates the document
    '''
    
    url: str = f'{uri}/{db}'
    
    params = {}
    
    if batch is not None:
        params['batch'] = batch

    async with ClientSession() as session:
        try:
            async with session.post(url, json=doc, params=params) as resp:
                if resp.status in (201, 202):
                    data = await resp.json()
                    res = PostDbOk(**data)
                elif resp.status == 400:
                    res = PostDbErr('Bad Request', 'Invalid database name')  # pragma: no cover
                elif resp.status == 401:
                    res = PostDbErr('Unauthorized', 'Write privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = PostDbErr('Not Found', 'Database doesn’t exist')
                elif resp.status == 409:
                    res = PostDbErr('Conflict', 'A Conflicting Document with same ID already exists')
                else:
                    res = PostDbErr('Status Error', f'Unknown Status Error: {resp.status}')
        except Exception as e:
            res = PostDbErr('Exception', e)

    if isinstance(res, PostDbErr):
        raise ResultException(res)
    
    return res

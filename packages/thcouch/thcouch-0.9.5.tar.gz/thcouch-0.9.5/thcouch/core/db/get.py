'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/common.html#get--db
'''
__all__ = ['GetDbResult', 'GetDbOk', 'GetDbErr', 'get_db']

from dataclasses import dataclass
from typing import TypedDict
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetDbOk:
    cluster: TypedDict('cluster', n=int, q=int, r=int, w=int)
    compact_running: bool
    db_name: str
    disk_format_version: int
    doc_count: int
    doc_del_count: int
    instance_start_time: str
    purge_seq: str
    sizes: TypedDict('sizes', active=int, external=int, file=int)
    update_seq: str
    props: TypedDict('props', partitioned=bool)


@dataclass
class GetDbErr:
    error: str
    reason: str


GetDbResult: type = Ok[GetDbOk] | Err[GetDbErr]


@GetDbResult[GetDbOk, GetDbErr]
async def get_db(uri: str, db: str) -> GetDbOk:
    '''
    This function gets information about the specified database
    '''
    
    url: str = f'{uri}/{db}'

    async with ClientSession() as session:        
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = GetDbOk(**data)
                elif resp.status == 404:
                    res = GetDbErr('Not Found', 'Requested database not found')
                else:
                    res = GetDbErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = GetDbErr('Exception', e)

    if isinstance(res, GetDbErr):
        raise ResultException(res)

    return res

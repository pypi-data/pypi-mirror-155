'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/find.html#post--db-_index
'''
__all__ = ['IndexResult', 'IndexOk', 'IndexErr', 'post_index']

from dataclasses import dataclass
from aiohttp import ClientSession
from typing import TypeAlias

from thresult import Ok, Err, ResultException


@dataclass
class IndexOk:
    result: str
    id: str
    name: str


@dataclass
class IndexErr:
    error: str
    reason: str


IndexResult: type = Ok[IndexOk] | Err[IndexErr]


@IndexResult[IndexOk, IndexErr]
async def post_index(uri: str,
                     db: str,
                     index: dict,
                     ddoc: str | None=None,
                     name: str | None=None,
                     type: str='json', # 'json' or 'text'
                     partial_filter_selector: dict | None=None,
                     partitioned: bool | None=None) -> IndexOk:
    '''
    This function creates the Index to database
    '''
    url: str = f'{uri}/{db}/_index'

    req_data = {
        'index': index,
        'type': type,
    }

    if ddoc is not None:
        req_data['ddoc'] = ddoc

    if name is not None:
        req_data['name'] = name

    if partial_filter_selector is not None:
        req_data['partial_filter_selector'] = partial_filter_selector

    if partitioned is not None:
        req_data['partitioned'] = partitioned
        
    async with ClientSession() as session:
        try:
            async with session.post(url, json=req_data) as resp:
                data: dict = await resp.json()

                if resp.status == 200:
                    res = IndexOk(**data)
                elif resp.status == 400:
                    res = IndexErr('Bad Request', 'Invalid request')                    
                elif resp.status == 401:
                    res = IndexErr('Unauthorized', 'Admin permission required')  # pragma: no cover
                elif resp.status == 404:
                    res = IndexErr('Not Found', 'Specified database nor found')
                elif resp.status == 500:
                    res = IndexErr('Internal Server Error', 'Execution error')  # pragma: no cover
                else:
                    res = IndexErr('Unknown Error', f'Unrecognized CouchDB status: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = IndexErr('Exception', e)

    if isinstance(res, IndexErr):
        raise ResultException(res)

    return res

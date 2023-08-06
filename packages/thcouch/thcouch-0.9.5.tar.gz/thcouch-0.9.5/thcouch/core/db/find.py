'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/find.html#post--db-_find
'''
__all__ = ['FindDbResult', 'FindDbOk', 'FindDbErr', 'find_db']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class FindDbOk:
    docs: list[dict]
    bookmark: str
    warning: str


@dataclass
class FindDbErr:
    error: str
    reason: str


FindDbResult: type = Ok[FindDbOk] | Err[FindDbErr]


@FindDbResult[FindDbOk, FindDbErr]
async def find_db(uri: str,
                  db: str,
                  selector: dict,
                  limit: int | None=None,
                  skip: int | None=None,
                  sort: list[dict | str] | None=None,
                  fields: list[str] | None=None,
                  use_index: (str | list[str]) | None=None,
                  r: int | None=None,
                  bookmark: str | None=None,
                  update: bool | None=None,
                  stable: bool | None=None,) -> FindDbOk:
    '''
    This function finds all docs from database
    '''

    url: str = f'{uri}/{db}/_find'

    req_data: dict = {
        'selector': selector,
    }

    if limit is not None:
        req_data['limit'] = limit

    if skip is not None:
        req_data['skip'] = skip

    if sort is not None:
        req_data['sort'] = sort  # pragma: no cover

    if fields is not None:
        req_data['fields'] = fields

    if use_index is not None:
        req_data['use_index'] = use_index

    if r is not None:
        req_data['r'] = r  # pragma: no cover

    if bookmark is not None:
        req_data['bookmark'] = bookmark  # pragma: no cover

    if update is not None:
        req_data['update'] = update

    if stable is not None:
        req_data['stable'] = stable
    
    async with ClientSession() as session:
        try:
            async with session.post(url, json=req_data) as resp:                   
                if resp.status == 200:
                    data: dict = await resp.json()
                    res = FindDbOk(**data)
                elif resp.status == 400:
                    res = FindDbErr('Bad Request', 'Invalid request')  # pragma: no cover
                elif resp.status == 401:
                    res = FindDbErr('Unauthorized', 'Read permission required')  # pragma: no cover
                elif resp.status == 404:
                    res = FindDbErr('Not Found', 'Requested database not found')
                elif resp.status == 500: # pragma: no cover
                    res = FindDbErr('500 Internal Server Error', 'Query execution error')  # pragma: no cover
                else:
                    res = FindDbErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = FindDbErr('Exception', e)
            
    if isinstance(res, FindDbErr):
        raise ResultException(res)
    
    return res

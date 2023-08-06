'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/find.html#delete--db-_index-designdoc-json-name
'''
__all__ = ['DeleteIndexResult', 'DeleteIndexOk', 'DeleteIndexErr', 'delete_index']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class DeleteIndexOk:
    ok: str


@dataclass
class DeleteIndexErr:
    error: str
    reason: str
    

DeleteIndexResult: type = Ok[DeleteIndexOk] | Err[DeleteIndexErr]


@DeleteIndexResult[DeleteIndexOk, DeleteIndexErr]
async def delete_index(uri: str, db: str, name: str, designdoc: str | None=None) -> DeleteIndexOk:
    '''
    This function deletes the Index from database by given index name  
    '''
    url: str = f'{uri}/{db}/_index/{designdoc}/json/{name}'

    async with ClientSession() as session:
        try:
            async with session.delete(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = DeleteIndexOk(**data)
                elif resp.status == 400:
                    res = DeleteIndexErr('Bad Request', 'Invalid request')  # pragma: no cover
                elif resp.status == 401:
                    res = DeleteIndexErr('Unauthorized', 'Writer permission required')  # pragma: no cover
                elif resp.status == 404:
                    res = DeleteIndexErr('Not Found', 'Index not found')
                elif resp.status == 500:
                    res = DeleteIndexErr('500 Internal Server Error', 'Execution error')  # pragma: no cover
                else:
                    res = DeleteIndexErr('Unknown Error', f'UUnrecognized CouchDB status: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = DeleteIndexErr('Exception', e)

    if isinstance(res, DeleteIndexErr):
        raise ResultException(res)
    
    return res

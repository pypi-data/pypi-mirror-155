'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
'''
__all__ = ['DeleteDocResult', 'DeleteDocOk', 'DeleteDocErr', 'delete_doc']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class DeleteDocOk:
    id: str
    ok: bool
    rev: str


@dataclass
class DeleteDocErr:
    error: str
    reason: str


DeleteDocResult: type = Ok[DeleteDocOk] | Err[DeleteDocErr]


@DeleteDocResult[DeleteDocOk, DeleteDocErr]
async def delete_doc(uri: str, db: str, docid: str, rev: str, batch: str | None=None) -> DeleteDocOk:
    '''
    This function deletes the doc from database by given docid and rev (latest)
    '''
    url: str = f'{uri}/{db}/{docid}'
    params = {}
    params['rev'] = rev

    # batch is optional query parameter and can be none or 'ok'
    if batch is not None:
        params['batch'] = batch
    
    async with ClientSession() as session:
        try:
            async with session.delete(url, params=params) as resp:
                if resp.status in (200, 202):
                    data = await resp.json()
                    res = DeleteDocOk(**data)
                elif resp.status == 400:
                    res = DeleteDocErr('Bad Request', 'Invalid request body or parameters')  # pragma: no cover
                elif resp.status == 401:
                    res = DeleteDocErr('Unauthorized', 'Write privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = DeleteDocErr('Not Found', 'Specified database or document ID doesn’t exists')
                elif resp.status == 409:
                    res = DeleteDocErr('Conflict', 'Specified revision is not the latest for target document')
                else:
                    res = DeleteDocErr('Unknown error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = DeleteDocErr('Exception', e)

    if isinstance(res, DeleteDocErr):
        raise ResultException(res)

    return res

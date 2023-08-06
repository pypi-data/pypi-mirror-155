'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-bulk-get
'''
__all__ = ['BulkGetResult', 'BulkGetOk', 'BulkGetErr', 'bulk_get']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class BulkGetOk:
    results: list[dict]


@dataclass
class BulkGetErr:
    error: str
    reason: str


BulkGetResult: type = Ok[BulkGetOk] | Err[BulkGetErr]


@BulkGetResult[BulkGetOk, BulkGetErr]
async def bulk_get(uri: str, db: str, docs: list[dict], revs: bool | None=None) -> BulkGetOk:
    """
    This method can be called to query several documents in bulk.
    It is well suited for fetching a specific revision of documents,
    as replicators do for example, or for getting revision history
    """
    url = f'{uri}/{db}/_bulk_get'

    req_data = {
        'docs': docs
    }

    params = {}
    if revs is not None and revs == 'True' or revs == 'true' or revs is True:
        params['revs'] = 'true'

    async with ClientSession() as session:
        try:
            async with session.post(url, json=req_data, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = BulkGetOk(**data)
                elif resp.status == 400:
                    res = BulkGetErr('Bad Request', 'The request provided invalid data or invalid query parameter')  # pragma: no cover
                elif resp.status == 401:
                    res = BulkGetErr('Unauthorized', 'Read permission required')  # pragma: no cover
                elif resp.status == 404:
                    res = BulkGetErr('Not Found', 'Database doesn’t exist')
                elif resp.status == 415: # pragma: no cover
                    res = BulkGetErr('Unsupported Media Type', 'Bad Content-Type value')  # pragma: no cover
                else:
                    res = BulkGetErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = BulkGetErr('Exception', e)
            
    if isinstance(res, BulkGetErr):
        raise ResultException(res)
    
    return res

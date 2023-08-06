'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-bulk-docs
    https://docs.couchdb.org/en/stable/replication/protocol.html?highlight=2.4.2.5.2#upload-batch-of-changed-documents
    https://github.com/apache/couchdb-documentation/issues/390
'''
__all__ = ['BulkDocsResult', 'BulkDocsOk', 'BulkDocsErr', 'bulk_docs']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class BulkDocsOk:
    results: list[dict]


@dataclass
class BulkDocsErr:
    error: str
    reason: str


BulkDocsResult: type = Ok[BulkDocsOk] | Err[BulkDocsErr]


@BulkDocsResult[BulkDocsOk, BulkDocsErr]
async def bulk_docs(uri: str, db: str, docs: list[dict], new_edits: bool | None=None) -> BulkDocsOk:
    '''
    The bulk docs function allows you to create and update multiple documents at the same time within a single request
    '''
    url = f'{uri}/{db}/_bulk_docs'

    req_data  = {
        'docs': docs
    }

    if new_edits is None:
        req_data['new_edits'] = True
    else:
        req_data['new_edits'] = new_edits

    async with ClientSession() as session:
        try:
            async with session.post(url, json=req_data) as resp:
                if resp.status == 201:
                    data = {}
                    data['results'] = await resp.json()
                    res = BulkDocsOk(**data)
                elif resp.status == 400:
                    res = BulkDocsErr('Bad Request', 'The request provided invalid JSON data')
                elif resp.status == 404:
                    res = BulkDocsErr('Not Found', 'Requested database not found')
                else:
                    res = BulkDocsErr('Status Error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = BulkDocsErr('Exception', e)
            
    if isinstance(res, BulkDocsErr):
        raise ResultException(res)
    
    return res



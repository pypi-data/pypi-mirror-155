'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
'''
__all__ = ['PutDocResult', 'PutDocOk', 'PutDocErr', 'put_doc']

import json
from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class PutDocOk:
    id: str
    ok: bool
    rev: str | None = None


@dataclass
class PutDocErr:
    error: str
    reason: str


PutDocResult: type = Ok[PutDocOk] | Err[PutDocErr]


@PutDocResult[PutDocOk, PutDocErr]
async def put_doc(uri: str,
                  db: str,
                  docid: str,
                  doc: dict,
                  rev: str | None=None,
                  batch: str | None=None,
                  new_edits: bool | None=None) -> PutDocOk:
    '''
    This function creates/updates the doc to/from database by given docid
    '''
    url: str = f'{uri}/{db}/{docid}'
    params = {}
    
    if rev is not None:
        params['rev'] = rev
    
    # batch (string) – Stores document in batch mode. Possible values: ok. Optional
    if batch is not None:
        params['batch'] = batch
    
    # new_edits (boolean) – Prevents insertion of a conflicting document.
    # Possible values: true (default) and false.
    # If false, a well-formed _rev must be included in the document.
    # new_edits=false is used by the replicator to insert documents into
    # the target database even if that leads to the creation of conflicts. Optional
    if new_edits is not None:
        params['new_edits'] = json.dumps(new_edits)

    async with ClientSession() as session:
        try:
            async with session.put(url, params=params, json=doc) as resp:
                if resp.status in (201, 202):
                    data = await resp.json()
                    res = PutDocOk(**data)
                elif resp.status == 400:
                    res = PutDocErr('Bad Request', 'Invalid request body or parameters')  # pragma: no cover
                elif resp.status == 401:
                    res = PutDocErr('Unauthorized', 'Write privileges required')  # pragma: no cover
                elif resp.status == 404:
                    res = PutDocErr('Not Found', 'Specified database or document ID doesn’t exists')
                elif resp.status == 409:
                    res = PutDocErr('Conflict', 'Document with the specified ID already exists or specified')
                else:
                    res = PutDocErr('Unknown error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = PutDocErr('Exception', e)

    if isinstance(res, PutDocErr):
        raise ResultException(res)
    
    return res
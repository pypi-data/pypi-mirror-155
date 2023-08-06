'''
Reference:
    https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
'''
__all__ = ['GetDocResult', 'GetDocOk', 'GetDocErr', 'get_doc']

import json
from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetDocOk:
    doc: dict


@dataclass
class GetDocErr:
    error: str
    reason: str


GetDocResult: type = Ok[GetDocOk] | Err[GetDocErr]

# FIXME: Function raises Exception (ContentTypeError) when param 'attachments' is set to True
@GetDocResult[GetDocOk, GetDocErr]
async def get_doc(uri: str, 
                  db: str, 
                  docid: str, 
                  attachments: bool | None=None,
                  att_encoding_info: bool | None=None,
                  atts_since: list | None=None,
                  conflicts: bool | None=None,
                  deleted_conflicts: bool | None=None,
                  latest: bool | None=None,
                  local_seq: bool | None=None,
                  meta: bool | None=None,
                  open_revs: list | None=None,
                  rev: str | None=None,
                  revs: bool | None=None,
                  revs_info: bool | None=None) -> GetDocOk:
    '''
    This function gets the doc from database by given docid
    '''
    url: str = f'{uri}/{db}/{docid}'
    params: dict = {}

    if attachments is not None:
        params['attachments'] = json.dumps(attachments)
    
    if att_encoding_info is not None:
        params['att_encoding_info'] = json.dumps(att_encoding_info)
    
    if atts_since is not None:
        params['atts_since'] = json.dumps(atts_since)
    
    if conflicts is not None:
        params['conflicts'] = json.dumps(conflicts)
    
    if deleted_conflicts is not None:
        params['deleted_conflicts'] = json.dumps(deleted_conflicts)
    
    if latest is not None:
        params['latest'] = json.dumps(latest)
    
    if local_seq is not None:
        params['local_seq'] = json.dumps(local_seq)
    
    if meta is not None:
        params['meta'] = json.dumps(meta)
    
    if open_revs is not None:
        params['open_revs'] = json.dumps(open_revs)
    
    if rev is not None:
        params['rev'] = rev
    
    if revs is not None:
        params['revs'] = json.dumps(revs)
    
    if revs_info is not None:
        params['revs_info'] = json.dumps(revs_info)
    

    async with ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                if resp.status in (200, 304):
                    data = await resp.json()
                    res = GetDocOk(data)
                elif resp.status == 400:
                    res = GetDocErr('Bad Request', 'The format of the request or revision was invalid')  # pragma: no cover
                elif resp.status == 401:
                    res = GetDocErr('Unauthorized', 'Read privilege required')  # pragma: no cover
                elif resp.status == 404:
                    res = GetDocErr('Not Found', 'Document not found')
                else:
                    res = GetDocErr('Unknown error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = GetDocErr('Exception', e)

    if isinstance(res, GetDocErr):
        raise ResultException(res)

    return res

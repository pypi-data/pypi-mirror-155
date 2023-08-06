'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-design-docs
'''
__all__ = ['GetDesignDocsOk', 'GetDesignDocsErr', 'GetDesignDocsResult', 'get_design_docs']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetDesignDocsOk:
    offset: int
    rows: list[dict]
    total_rows: int


@dataclass
class GetDesignDocsErr:
    error: str
    reason: str


GetDesignDocsResult: type = Ok[GetDesignDocsOk] | Err[GetDesignDocsErr]


@GetDesignDocsResult[GetDesignDocsOk, GetDesignDocsErr]
async def get_design_docs(uri: str,
                          db: str,
                          conflicts: None | bool=None,
                          descending: None | bool=None,
                          end_key: None | str=None,
                          end_key_doc_id: None | str=None,
                          include_docs: None | bool=None,
                          inclusive_end: None | bool=None,
                          key: None | str=None,
                          keys: None | str=None,
                          limit: None | int=None,
                          skip: None | int=None,
                          start_key: None | str=None,
                          start_key_doc_id: None | str=None,
                          update_seq: None | bool=None) -> GetDesignDocsOk:
    '''
    This function gets the designdocument from database
    '''
    url: str = f'{uri}/{db}/_design_docs'
    params = {}

    if conflicts is not None:
        params['conflicts'] = conflicts

    if descending is not None:
        params['descending'] = descending

    if end_key is not None:
        params['end_key'] = end_key

    if end_key_doc_id is not None:
        params['end_key_doc_id'] = end_key_doc_id

    if inclusive_end is not None:
        params['inclusive_end'] = inclusive_end

    if key is not None:
        params['key'] = key

    if keys is not None:
        params['keys'] = keys

    if limit is not None:
        params['limit'] = limit

    if skip is not None:
        params['skip'] = skip

    if start_key is not None:
        params['start_key'] = start_key

    if start_key_doc_id is not None:
        params['start_key_doc_id'] = start_key_doc_id

    if update_seq is not None:
        params['update_seq'] = update_seq

    async with ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = GetDesignDocsOk(**data)
                elif resp.status == 404:
                    res = GetDesignDocsErr('Not Found', 'Requested database not found')
                else:
                    res = GetDesignDocsErr('Status error', f'Unknown Status Error: {resp.status}') # pragma: no cover
        except Exception as e:
            res = GetDesignDocsErr('Exception', e)
            
    if isinstance(res, GetDesignDocsErr):
        raise ResultException(res)

    return res

'''
Reference:
    https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_design_docs
'''
__all__ = ['PostDesignDocsOk', 'PostDesignDocsErr', 'PostDesignDocsResult', 'post_design_docs']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class PostDesignDocsOk:
    offset: int
    rows: list[dict]
    total_rows: int


@dataclass
class PostDesignDocsErr:
    error: str
    reason: str


PostDesignDocsResult: type = Ok[PostDesignDocsOk] | Err[PostDesignDocsErr]


@PostDesignDocsResult[PostDesignDocsOk, PostDesignDocsErr]
async def post_design_docs(uri: str,
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
                           update_seq: None | bool=None) -> PostDesignDocsOk:
    '''
    This function supports identical parameters and behavior as get_design_docs
    but allows for the query string parameters to be supplied as keys in a JSON 
    object in the body of the POST request
    '''
    url: str = f'{uri}/{db}/_design_docs'
    req_json = {}

    if conflicts is not None:
        req_json['conflicts'] = conflicts

    if descending is not None:
        req_json['descending'] = descending

    if end_key is not None:
        req_json['end_key'] = end_key

    if end_key_doc_id is not None:
        req_json['end_key_doc_id'] = end_key_doc_id

    if inclusive_end is not None:
        req_json['inclusive_end'] = inclusive_end

    if key is not None:
        req_json['key'] = key

    if keys is not None:
        req_json['keys'] = keys

    if limit is not None:
        req_json['limit'] = limit

    if skip is not None:
        req_json['skip'] = skip

    if start_key is not None:
        req_json['start_key'] = start_key

    if start_key_doc_id is not None:
        req_json['start_key_doc_id'] = start_key_doc_id

    if update_seq is not None:
        req_json['update_seq'] = update_seq

    async with ClientSession() as session:
        try:
            async with session.post(url, json=req_json) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = PostDesignDocsOk(**data)
                elif resp.status == 404:
                    res = PostDesignDocsErr('Not Found', 'Requested database not found')
                else:
                    res = PostDesignDocsErr('Status error', f'Unknown Status Error: {resp.status}') # pragma: no cover
        except Exception as e:
            res = PostDesignDocsErr('Exception', e)
            
    if isinstance(res, PostDesignDocsErr):
        raise ResultException(res)

    return res

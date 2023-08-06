'''
Reference:
    https://docs.couchdb.org/en/stable/api/server/common.html#get--_all_dbs
'''
__all__ = ['GetAllDbsOk', 'GetAllDbsErr', 'GetAllDbsResult', 'get_all_dbs']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException
  
  
@dataclass
class GetAllDbsOk:
    dbs: list[str]


@dataclass
class GetAllDbsErr:
    error: str
    reason: str


GetAllDbsResult: type = Ok[GetAllDbsOk] | Err[GetAllDbsErr]


@GetAllDbsResult[GetAllDbsOk, GetAllDbsErr]
async def get_all_dbs(uri: str, descending: bool | None=None | str | int,
                      end_key: int | None=None,
                      limit: int | None=None,
                      skip: int | None=None,
                      start_key: str | None=None) -> GetAllDbsOk:
    '''
    This function gets all databases 
    '''
    url: str = f'{uri}/_all_dbs'
    params = {}

    if descending is not None and descending == 'True' or descending is True:
        params['descending'] = 'True'

    if end_key is not None:
        params['end_key'] = end_key

    if limit is not None:
        params['limit'] = limit

    if skip is not None:
        params['skip'] = skip

    if start_key is not None:
        params['start_key'] = start_key

    async with ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = GetAllDbsOk(data)
                else:
                    res = GetAllDbsErr('Unknown Error', 'Could not get all databases')  # pragma: no cover
        except Exception as e:
            res = GetAllDbsErr('Exception', e)
    
    if isinstance(res, GetAllDbsErr):
        raise ResultException(res)

    return res
    
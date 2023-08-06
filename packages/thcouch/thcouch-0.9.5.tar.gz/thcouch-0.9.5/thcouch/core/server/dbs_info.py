'''
Reference:
    https://docs.couchdb.org/en/stable/api/server/common.html#dbs-info
'''
__all__ = ['GetDbsInfoOk', 'GetDbsInfoErr', 'GetDbsInfoResult', 'post_dbs_info']

from dataclasses import dataclass
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetDbsInfoOk:
    dbs_info: list[dict]


@dataclass
class GetDbsInfoErr:
    error: str
    reason: str


GetDbsInfoResult: type = Ok[GetDbsInfoOk] | Err[GetDbsInfoErr]


@GetDbsInfoResult[GetDbsInfoOk, GetDbsInfoErr]
async def post_dbs_info(uri: str, keys: list[str]) -> GetDbsInfoOk:
    '''
    This function returns information of a list of the specified databases
    '''
    url: str = f'{uri}/_dbs_info'

    request_data = {}
    request_data['keys'] = keys

    async with ClientSession() as session:
        try:
            async with session.post(url, json=request_data) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    resp_dict = {}
                    resp_dict['dbs_info'] = data
                    res = GetDbsInfoOk(**resp_dict)
                elif resp.status == 400:
                    res = GetDbsInfoErr('Bad Request', 'Missing keys or exceeded keys in request')
                else:
                    res = GetDbsInfoErr('Unknown error', f'Unknown Status Error: {resp.status}')  # pragma: no cover
        except Exception as e:
            res = GetDbsInfoErr('Exception', e)

    if isinstance(res, GetDbsInfoErr):
        raise ResultException(res)

    return res
    
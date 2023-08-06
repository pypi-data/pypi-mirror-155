'''
Reference:
    https://docs.couchdb.org/en/stable/api/server/common.html
'''
__all__ = ['GetServerOk', 'GetServerErr', 'GetServerResult', 'get_server']

from dataclasses import dataclass
from typing import TypedDict
from aiohttp import ClientSession

from thresult import Ok, Err, ResultException


@dataclass
class GetServerOk:
    couchdb: str
    git_sha: str
    features: list[str]
    uuid: str
    vendor: TypedDict('vendor', name=str, version=str)
    version: str


@dataclass
class GetServerErr:
    error: str
    reason: str


GetServerResult: type = Ok[GetServerOk] | Err[GetServerErr]


@GetServerResult[GetServerOk, GetServerErr]
async def get_server(uri: str) -> GetServerOk:
    '''
    This function gets the server   
    '''
    url: str = f'{uri}'
    async with ClientSession() as session:   
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    res = GetServerOk(**data)
                else:
                    res = GetServerErr('Unknown Error', 'Could not connect to server')  # pragma: no cover
        except Exception as e:
            res = GetServerErr('Exception', e)

    if isinstance(res, GetServerErr):
        raise ResultException(res)

    return res

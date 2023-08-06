__all__ = ['CouchLoader']

import os
import json
import json5
import toml
import yaml

from uuid import uuid4
from typing import Any, TypeVar
from os.path import splitext
from collections import ChainMap

from thcouch.orm import CouchDatabase
from thcouch.orm.decl import BaseModel, BaseObject, BaseIndex, Field
from thcouch.orm.decl.error import FileConfigError, CouchLoaderError


class CouchLoader:
    _db: CouchDatabase
    _path: None | str
    _schema: dict
    _types: dict[str, Any]
    _models: dict[str, BaseModel]
    _objects: dict[str, BaseObject]
    _indexes: dict[str, BaseIndex]
    _ns: ChainMap


    def __init__(self, db: CouchDatabase, path: None | str=None, schema: None | dict=None):
        self._db = db
        self._path = path

        if path and not schema:

            if not os.path.exists(self._path):
                raise FileConfigError(f'Path not found {self._path!r}')

            with open(self._path) as f:
                _, ext_ = splitext(self._path)
                ext_: str = ext_[1:]

                match ext_:
                    case 'toml':
                        schema = toml.load(f)
                    case 'yaml':
                        schema = yaml.safe_load(f)
                    case 'json':
                        schema = json.load(f)
                    case 'json5':
                        schema = json5.load(f)
                    case _:
                        raise CouchLoaderError(f'Unsupported file type. '
                                               f'Expected toml, yaml, json or json5 file, got {ext_}')

            for k, v in schema.items():
                _type = v.get('_type', 'model')

            self._schema = schema
        elif not path and schema:
            self._schema = schema
        else:
            raise CouchLoaderError(f'path or schema expected, either one but not both')

        self._types = {
            'Field': Field,
            'none': type(None),
            'bool': bool,
            'boolean': bool,
            'str': str,
            'string': str,
            'int': int,
            'integer': int,
            'float': float,
            'number': float,
            'tuple': tuple,
            'list': list,
            'array': list,
            'dict': dict,
            'object': dict,
            'uuid4': (lambda: str(uuid4())),
        }

        self._models = {}
        self._objects = {}
        self._indexes = {}
        self._ns = ChainMap(self._types, self._models, self._objects, self._indexes)

        # force caching
        for k, v in schema.items():
            getattr(self, k)
    

    def __getattr__(self, attr: str) -> type:
        _models = self.__dict__['_models']
        _objects = self.__dict__['_objects']
        _indexes = self.__dict__['_indexes']
        _schema = self.__dict__['_schema']
        _ns = self.__dict__['_ns']
        type_params: list[str] = []
        original_attr: str = attr

        # check generics' types in name of entity
        if '[' in attr and ']' in attr:
            attr, rest = attr[:attr.index('[')], attr[attr.index('['):]
            attr = attr.strip()
            rest = rest[rest.index('[') + 1:rest.index(']')]
            type_params = [r.strip() for r in rest.split(',')]

        # check models cache
        if attr in _models:
            return _models[attr]

        # check objects cache
        if attr in _objects:
            return _objects[attr]

        # check indexes cache
        if attr in _indexes:
            return _indexes[attr]

        # check if document or index
        model_schema = _schema[original_attr]
        _type = model_schema.get('_type', 'model')
        
        # eval globals and locals
        eval_globals = _ns
        eval_locals = {}

        def _patch_type(k: str, t: str) -> str:
            # eliminate beginning and ending spaces 
            t = t.strip()

            # strip "Field(" and ")"
            if t.startswith('Field(') and t.endswith(')'):
                t = t[len('Field('):-1]

            # add default name if not present
            if 'name' not in [n.strip().split('=')[0] for n in t.split(',') if '=' in n]:
                t += f', name={k!r}'

            # encapsulate Field
            t = f'Field({t})'
            return t

        def _eval_field(k: str, t: str) -> Field:
            t: str = _patch_type(k, t)
            field: Field = eval(t, eval_locals, eval_globals)
            field.set_original_def_code(t)
            return field

        if _type == 'model':
            model_schema['_attachments'] = 'dict, default={}'
            # declare model
            type_name = attr
            type_bases = (BaseModel,)
            type_params = model_schema.get('_type_params', type_params)
            
            # create generic types' placeholders
            for type_param in type_params:
                eval_locals[type_param] = TypeVar(type_param)

            type_dict = {
                'loader': self,
                'type_params': type_params,
                'ns': eval_locals,
                'fields': {
                    k: _eval_field(k, t)
                    for k, t in model_schema.items()
                    if k not in ('_type', '_type_params')
                },
            }

            model_type: type = type(type_name, type_bases, type_dict)

            # cache model
            _models[attr] = model_type

            # return model
            return model_type
        elif _type == 'object':
            # decalre object
            type_name = attr
            type_bases = (BaseObject,)
            type_params = model_schema.get('_type_params', type_params)
            
            # create generic types' placeholders
            for type_param in type_params:
                eval_locals[type_param] = TypeVar(type_param)

            type_dict = {
                'loader': self,
                'type_params': type_params,
                'ns': eval_locals,
                'fields': {
                    k: _eval_field(k, t)
                    for k, t in model_schema.items()
                    if k not in ('_type', '_type_params')
                },
            }

            object_type: type = type(type_name, type_bases, type_dict)

            # cache object
            _objects[attr] = object_type

            # return object
            return object_type
        elif _type == 'index':
            index_name = attr
            index_bases = (BaseIndex,)
            index_dict = {}
            
            for key in _schema[attr]:
                if key != '_type':
                    index_dict[key] = _schema[attr][key]

            index_dict['name'] = attr
            index_dict['loader'] = self
            index_type: type = type(index_name, index_bases, index_dict)

            # cache index
            _indexes[attr] = index_type
            return index_type
        else:
            raise ValueError(f'unsupported _type: {_type!r}')


    def __getitem__(self, attr: str) -> type:
        return getattr(self, attr)

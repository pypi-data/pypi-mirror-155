__all__ = ['BaseObject']

from copy import deepcopy
from typing import Any, TypeAlias

from thresult import Result, Ok, Err

from .field import Field


BaseObject: TypeAlias = 'BaseObject'
CouchLoader: TypeAlias = 'CouchLoader'


class BaseObjectType(type):
    def __repr__(cls) -> str:
        if hasattr(cls, 'fields'):
            pairs = ', '.join(f'{k}={v!r}' for k, v in cls.fields.items())
            return f'<class object {cls.__name__} {pairs} at {hex(id(cls))}>'

        return f'<class object {cls.__name__} at {hex(id(cls))}>'


    def __getitem__(cls, spec_type_params):
        if not isinstance(spec_type_params, tuple):
            spec_type_params = (spec_type_params,)
        # specialize types of generics
        type_params = dict(zip(cls.type_params, spec_type_params))
        new_ns = deepcopy(cls.ns) | type_params
        
        new_fields = {}
        
        for field_name, field in cls.fields.items():
            new_field: Field = eval(field.def_code, new_ns, cls.loader._ns)
            new_fields[field_name] = new_field

        new_ns: dict[str, Any] = deepcopy(cls.ns)
        # TODO: @Marko_Tasic - New type name should contain only fields found in type_params,
        #  ignoring redundant fields which might be found in spec_type_params?
        # new_type_name: str = f'{cls.__name__}{list(spec_type_params)}'
        new_type_name: str = f'{cls.__name__}{list(type_params.values())}'
        new_type_bases: tuple[type] = (cls,)

        new_type_dict: dict = {
            'loader': cls.loader,
            'type_params': cls.type_params,
            'ns': new_ns,
            'fields': new_fields,
        }

        new_cls: type = type(new_type_name, new_type_bases, new_type_dict)
        return new_cls

    
    def __instancecheck__(cls, obj) -> bool:
        O: type = type(obj)
        
        if not issubclass(O, BaseObject):
            return False

        if cls is BaseObject:
            return True

        if not issubclass(O, cls.__bases__):
            return False

        if hasattr(cls, 'type_params') and hasattr(O, 'type_params') and cls.type_params and O.type_params and cls.type_params != O.type_params:
            return False

        return True


class BaseObject(metaclass=BaseObjectType):
    loader: CouchLoader         # class var
    type_params: list           # class var
    fields: dict[str, Field]    # class var
    entries: dict[str, Any]


    def __init__(self, **kwargs):
        self.entries = {}

        for k, t in self.fields.items():
            if k in kwargs:
                v = kwargs[k]
            else:
                if callable(t.default):
                    v = t.default()
                else:
                    v = t.default
            
            def _deser(v: Any) -> Any:
                if isinstance(v, dict) and '$collection' in v:
                    entity_cls_name = v['$collection']
                    entity_type = self.loader._ns[entity_cls_name]
                    v = entity_type(**v)
                elif isinstance(v, list):
                    v = [_deser(n) for n in v]
                return v

            v = _deser(v)
            self.entries[k] = v

        self.validate().unwrap()


    def __repr__(self) -> str:
        pairs = ', '.join(f'{k}={v!r}' for k, v in self.entries.items())
        return f'<{self.__class__.__name__} Object {pairs}>'


    def __getitem__(self, key: str) -> Any:
        return self.entries[key]


    def __getattr__(self, attr: str) -> Any:
        return self.entries[attr]


    def __copy__(self) -> dict:
        return self.asdict()
    

    def __deepcopy__(self, memo: Any) -> dict:
        return self.asdict()


    def validate(self) -> Result[BaseObject, str]:
        for k, v in self.entries.items():
            t = self.fields[k]

            match obj := t.validate(v):
                case Err(e):
                    return Err[str](f'{k}: {e}')

        return Ok[BaseObject](self)


    def asdict(self) -> dict:
        return {
            '$collection': str(self.__class__.__name__),
            **deepcopy({
                k: v
                for k, v in self.entries.items()
                if self.fields[k].should_get(v)
            })
        }


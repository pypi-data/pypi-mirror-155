__all__ = ['FieldValidator', 'DefaultFieldValidator', 'EmailFieldValidator']

import re

from types import UnionType
from typing import Any, TypeAlias

from thresult import Ok, Err


EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
email_regex = re.compile(EMAIL_REGEX)


Field: TypeAlias = 'Field'


class FieldValidator:
    def __init__(self):
        pass


    def __call__(self, field: Field, value: Any) -> (bool, str | None):
        if type(field.type_).__name__ == 'BaseObjectType':
            """
            # TODO: @MarkoTasic review needed for validation field Name and value Name check
            if value is not None:
                # value_name = value.__class__.__name__
                # if '[' in value_name:
                #     value_name = value_name[0:value_name.index('[')]
                value_name = value.__class__.__name__[0:value.__class__.__name__.index('[')] if '[' in value.__class__.__name__  else value.__class__.__name__
                
                field_name = field.type_.__name__
                
                if value_name != field_name:
                    raise ValueError(f'Failed field validation: got {value_name} expected {field_name}')
            """
            # return True, None
            match r := value.validate():
                case Ok(v):                    
                    if value is not None:
                        if isinstance(field.type_, type):
                            if not isinstance(value, field.type_):
                                return False, f'type [0]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
                        elif isinstance(field.type_, UnionType):
                            if not isinstance(value, field.type_):
                                return False, f'type [1]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
                        else:
                            return False, f'type: failed generic parametrized check, `field.type_` is not type/class, got {field.type_} of type {type(field.type_)}'
                    
                    return True, None
                case Err(e):  # pragma: no cover
                    return False, e

        # check if generic parametrized type
        if value is not None and hasattr(field.type_, '__origin__') and hasattr(field.type_, '__args__'):
            T: type = field.type_.__origin__
            TArgs: tuple[type] = field.type_.__args__

            if issubclass(T, tuple):
                if len(TArgs) == 1:
                    if isinstance(value, T) and all(isinstance(n, TArgs) for n in value):
                        return True, None  # ???
                    else:
                        return False, f'type: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
                elif len(TArgs) > 1:
                    if len(TArgs) != len(value):
                        return False, f'type: failed generic parametrized check, unequal length of value {value} and tuple type {field.type_}'

                    if not all(isinstance(v, t) for v, t in zip(value, TArgs)):
                        return False, f'type: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'

                    return True, None  # ???
            elif issubclass(T, list):
                if isinstance(value, T):
                    if all(isinstance(n, TArgs) for n in value):
                        return True, None  # ???
                    else:
                        return False, f'type [-2]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
                else:
                    return False, f'type [-3]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
            elif issubclass(T, dict):
                K, V = TArgs

                if isinstance(value, T) and all(isinstance(n, K) for n in value.keys()) and all(isinstance(n, V) for n in value.values()):
                    return True, None  # ???
                else:
                    return False, f'type: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
            else:
                return False, f'type: failed generic parametrized check, unknown type of `field.type_`, got {field.type_}'

        if value is not None:
            if isinstance(field.type_, type):
                if not isinstance(value, field.type_):
                    return False, f'type [2]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
            elif isinstance(field.type_, UnionType):
                if not isinstance(value, field.type_):
                    return False, f'type [3]: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
                """
                # TODO: @MarkoTasic review needed for validation field Name and value Name check for BaseObject Type
                # value_name = value.__class__.__name__
                # if '[' in value_name:
                #     value_name = value_name[0:value_name.index('[')]
                value_name = value.__class__.__name__[0:value.__class__.__name__.index('[')] if '[' in value.__class__.__name__  else value.__class__.__name__

                # field_names_tuple = get_args(field.type_)
                # field_names = []
                #
                # for n in field.type_.__args__:
                #     field_names.append(n.__name__)
                field_names = [n.__name__ for n in field.type_.__args__]
                
                if value_name not in field_names:
                    raise ValueError(f'Failed field validation: got value {value} of type {value_name} expected {field_names}')
                """
            else:
                return False, f'type: failed generic parametrized check, `field.type_` is not type/class, got {field.type_} of type {type(field.type_)}'

        if field.required and value is None:
            return False, 'required, but not provided'

        if isinstance(field.values, (list, tuple)) and value not in field.values:
            return False, f'type: failed generic parametrized check, got value {value!r} of type {type(value)!r} but expected {field.type_!r}'
        
        return True, None


class DefaultFieldValidator(FieldValidator):
    def __call__(self, field: Field, value: Any) -> (bool, str | None):
        # valid: bool = FieldValidator.__call__(self, field, value)
        valid: (bool, str | None) = super().__call__(field, value)
        return valid


class EmailFieldValidator(FieldValidator):
    def __call__(self, field: Field, value: Any) -> (bool, str | None):
        valid: (bool, str | None) = super().__call__(field, value)
        status, msg = valid

        if not status:  # pragma: no cover
            return valid

        if not email_regex.search(value):
            return False, f'email validation failed, got {value!r}'

        return valid

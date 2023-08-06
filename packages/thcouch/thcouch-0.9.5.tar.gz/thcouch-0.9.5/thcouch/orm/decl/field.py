__all__ = ['Field']

from typing import Any, Callable, TypeAlias

from thresult import Result, Ok, Err

from .validator import EmailFieldValidator, DefaultFieldValidator


_field_validators = {
    'email': EmailFieldValidator(),
    'default': DefaultFieldValidator(),
}

Field: TypeAlias = 'Field'


class Field:
    type_: type
    name: str | None=None
    required: bool
    should_get: Callable | None
    default: Callable | object | None
    values: list | tuple | None
    validator: Callable | None
    def_code: str | None


    def __init__(self,
                 type_,
                 name: str | None=None,
                 required: bool=False,
                 should_get: Callable | None=None,
                 default: Callable | object | None=None,
                 values: list | tuple | None=None,
                 validator: Callable | None=None,
                 def_code: str | None=None):
        self.type_ = type_
        self.name = name
        self.required = required
        self.should_get = should_get if should_get else (lambda value: True)
        self.default = default
        self.values = values

        # FIXME: handle unsupported or errorous validator
        if isinstance(validator, str):
            validator = _field_validators.get(validator, _field_validators['default'])
        elif validator is None:
            validator = _field_validators['default']

        self.validator = validator
        self.def_code = def_code


    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} '
            f'type_={self.type_!r}, '
            f'name={self.name!r}, '
            f'required={self.required!r}, '
            f'should_get={self.should_get!r}, '
            f'default={self.default!r}, '
            f'values={self.values!r}, '
            f'validator={self.validator!r}>'
        )


    def __copy__(self) -> Field:
        return Field( # pragma: no cover
            type_=self.type_,
            name=self.name,
            required=self.required,
            should_get=self.should_get,
            default=self.default,
            values=self.values,
            validator=self.validator,
            def_code=self.def_code,
        )
    

    def __deepcopy__(self, memo: Any) -> Field:
        return Field( # pragma: no cover
            type_=self.type_,
            name=self.name,
            required=self.required,
            should_get=self.should_get,
            default=self.default,
            values=self.values,
            validator=self.validator,
            def_code=self.def_code,
        )


    # @classmethod
    # def new_from_def_code(self, def_code) -> Field:
        


    def validate(self, value) -> Result[Field, str]:
        valid: (bool, str | None) = self.validator(field=self, value=value)
        status, msg = valid
        res: Result

        if status:
            res = Ok[Field](self)
        else:
            res = Err[str](msg)

        return res


    def set_original_def_code(self, def_code: str):
        self.def_code = def_code

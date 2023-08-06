from __future__ import annotations
from typing import Any, Type, TypeVar, get_type_hints
from re import compile

T = TypeVar('T')


class AnonymousObject:

    def _cast_inner_value(self, value, type=None):
        if isinstance(value, list):
            result = [self._cast_inner_value(v, None if type is None or len(getattr(type, '__args__', [])) == 0 else type.__args__[0]) for v in value]
            if type:
                result = type(result)
            return result
        elif isinstance(value, AnonymousObject) and type is not None:
            return value.cast(type)
        elif type is not None:
            if issubclass(type, dict):
                return type(**value)
            return type(value)
        return value

    def cast(self, _type: Type[T]) -> T:
        types = get_type_hints(_type)
        return _type(**{
            key: self._cast_inner_value(value, types.get(key))
            for key, value in self.__dict__.items()
        })

    def __repr__(self):
        return "AnonymousObject({})".format(', '.join([
            '='.join([field, repr(value)])
            for field, value in self.__dict__.items()
        ]))


class PropertyAccessor:

    DICT_KEY_REGEX = compile(r'^\[["\'](?P<key>[\w+-]*)["\']\]')
    LIST_INDEX_REGEX = compile(r'^\[(?P<key>\d+)\]')
    PROPERTY_NAME_REGEX = compile(r'^[.]?(?P<property>[\w+-]*)')

    def __init__(self, data, create=True):
        self.data = data
        self._create = create

    def _recursive_get(self, data: Any, path: str):
        if not path:
            return data
        if match := self.DICT_KEY_REGEX.match(path):
            return self._recursive_get(data[match.group('key')], self.DICT_KEY_REGEX.sub('', path))
        if match := self.LIST_INDEX_REGEX.match(path):
            return self._recursive_get(data[int(match.group('key'))], self.LIST_INDEX_REGEX.sub('', path))
        if match := self.PROPERTY_NAME_REGEX.match(path):
            return self._recursive_get(getattr(data, match.group('property')), self.PROPERTY_NAME_REGEX.sub('', path))
        return data

    def get(self, path: str, *default):
        try:
            path_data = self._recursive_get(self.data, path)
            return path_data
        except:
            if default:
                return default[0]
            raise AttributeError(f'"{path}" is invalid path')

    def _recursive_set(self, data: Any, path: str, value: Any):
        if not path:
            return value
        if match := self.DICT_KEY_REGEX.match(path):
            if data is None and self._create:
                data = {}
            key = match.group('key')
            data[key] = self._recursive_set(data.get(key), self.DICT_KEY_REGEX.sub('', path), value)
        elif match := self.LIST_INDEX_REGEX.match(path):
            if data is None and self._create:
                data = []
            key = int(match.group('key'))
            if len(data) <= key:
                data.append(self._recursive_set(None, self.LIST_INDEX_REGEX.sub('', path), value))
            else:
                data[key] = self._recursive_set(data[key], self.LIST_INDEX_REGEX.sub('', path), value)
        elif match := self.PROPERTY_NAME_REGEX.match(path):
            if data is None and self._create:
                data = AnonymousObject()
            _property = match.group('property')
            setattr(data, _property, self._recursive_set(getattr(data, _property, None), self.PROPERTY_NAME_REGEX.sub('', path), value))
        return data

    def set(self, path: str, value: Any):
        self.data = self._recursive_set(self.data, path, value)
        return value


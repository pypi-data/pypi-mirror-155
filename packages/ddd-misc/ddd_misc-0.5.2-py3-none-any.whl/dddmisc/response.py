import typing as t
import json
from uuid import UUID
import datetime as dt

from dddmisc.messages.core import Nothing
from dddmisc.exceptions import JsonDecodeError
from dddmisc.aggregate import BaseAggregate

T = t.TypeVar('T', bound=BaseAggregate)


class DDDResponse(t.Generic[T]):

    def __init__(self, reference: UUID, aggregate: T = None):
        self._reference = reference
        self._timestamp = dt.datetime.now().timestamp()
        self._aggregate = aggregate

    @property
    def __domain__(self):
        return None

    @property
    def __reference__(self) -> UUID:
        """Идентификатор команды для которой предназначен ответ"""
        return self._reference

    @property
    def __timestamp__(self) -> float:
        return self._timestamp

    @property
    def aggregate(self) -> t.Optional[T]:
        return self._aggregate

    @classmethod
    def load(cls, data: dict):
        aggregate_ref = UUID(data.get('data', {}).get('reference', Nothing))
        aggregate = BaseAggregate(reference=aggregate_ref)
        reference = UUID(data['__reference__'])
        obj = cls(reference, aggregate)
        if ref_value := data.get('__reference__', None):
            obj._reference = UUID(ref_value)
        if ts_value := data.get('__timestamp__', None):
            obj._timestamp = ts_value
        return obj

    @classmethod
    def loads(cls, data):
        try:
            dict_data = json.loads(data)
            return cls.load(dict_data)
        except json.JSONDecodeError as err:
            raise JsonDecodeError(str(err))

    def dump(self):
        result = {
            '__reference__': str(self.__reference__),
            '__timestamp__': self.__timestamp__,
            'data': {'reference': str(self.aggregate.reference)}
        }
        return result

    def dumps(self):
        data = self.dump()
        return json.dumps(data)

    def __eq__(self, other):
        return isinstance(other, DDDResponse) and hash(self) == hash(other)

    def __hash__(self):
        return hash(f'DDDResponse.{self.aggregate.reference}.'
                    f'{self.__reference__}.{self.__timestamp__}')

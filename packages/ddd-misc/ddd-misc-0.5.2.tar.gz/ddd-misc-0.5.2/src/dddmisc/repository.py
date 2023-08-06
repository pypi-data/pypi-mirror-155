import abc
import typing as t
from uuid import UUID

from dddmisc import BaseAggregate


A = t.TypeVar('A', bound=BaseAggregate)
T = t.TypeVar('T')


class AbstractRepository(abc.ABC, t.Generic[A, T]):
    aggregate_class: t.Type[A]

    def __init__(self, connection: T):
        self._seen: set[A] = set()
        self._connection = connection
        self.events = set()

    @t.final
    def add(self, aggregate: A):
        if not isinstance(aggregate, self.aggregate_class):
            raise TypeError(fr'aggregate required be is instance of {self.aggregate_class!r}')
        if self._get_from_cache(aggregate.reference) is None:
            self._seen.add(aggregate)
        else:
            raise RuntimeError(f'aggregate {aggregate.reference} is exist')

    @t.final
    def _get_from_cache(self, reference: UUID) -> t.Optional[A]:
        return next((aggregate for aggregate in self._seen
                     if aggregate.reference == reference), None)

    @t.final
    def _collect_events(self):
        for aggregate in self._seen:
            self.events.update(aggregate.get_aggregate_events())

    @t.final
    def clear_events(self):
        self._collect_events()
        self.events.clear()


class AbstractAsyncRepository(AbstractRepository[A, T], abc.ABC):

    @abc.abstractmethod
    async def _add_to_storage(self, aggregate: A):
        ...

    @t.final
    async def get(self, reference: UUID) -> A:
        aggregate = self._get_from_cache(reference)
        if aggregate:
            return aggregate
        aggregate = await self._get_from_storage(reference)
        self._seen.add(aggregate)
        return aggregate

    @abc.abstractmethod
    async def _get_from_storage(self, reference: UUID) -> A:
        ...

    @t.final
    async def apply_changes(self):
        for aggregate in self._seen:
            await self._add_to_storage(aggregate)
        self._collect_events()


class AbstractSyncRepository(AbstractRepository[A, T], abc.ABC):

    @abc.abstractmethod
    def _add_to_storage(self, aggregate: A):
        ...

    @t.final
    def get(self, reference: UUID) -> A:
        aggregate = self._get_from_cache(reference)
        if aggregate:
            return aggregate
        aggregate = self._get_from_storage(reference)
        self._seen.add(aggregate)
        return aggregate

    @abc.abstractmethod
    def _get_from_storage(self, reference: UUID) -> A:
        ...

    @t.final
    def apply_changes(self):
        for aggregate in self._seen:
            self._add_to_storage(aggregate)
        self._collect_events()

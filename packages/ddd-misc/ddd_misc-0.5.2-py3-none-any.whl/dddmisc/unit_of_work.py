import abc
import typing as t

from dddmisc.messages import DDDEvent
from dddmisc.repository import AbstractSyncRepository, AbstractAsyncRepository

T = t.TypeVar('T')
R = t.TypeVar('R', bound=t.Union[AbstractSyncRepository, AbstractAsyncRepository])


class AbstractUnitOfWork(t.Generic[R, T]):
    repository_class: t.Type[R]
    _repository: R

    def __init__(self, engine: t.Any = None,
                 *, repository_class: t.Type[R] = None):
        self._engine = engine
        self._events: t.Set[DDDEvent] = set()
        self._current_transaction_events: t.Set[DDDEvent] = set()
        self._in_context = False
        self._repository_class = repository_class or type(self).repository_class
        self._connection: T = None

    @property
    def repository(self) -> R:
        if hasattr(self, '_repository'):
            return self._repository
        else:
            raise RuntimeError('Need enter to UnitOfWork context manager before access to "repository"')

    @t.final
    def collect_events(self) -> t.Tuple[DDDEvent]:
        """Отдаем все накопленные события"""
        events = tuple(sorted(self._events, key=lambda x: x.__timestamp__))
        self._events.clear()
        return events

    @t.final
    def _post_commit(self):
        """Добавляем события репозитория в набор событий по транзакции"""
        self._current_transaction_events.update(self.repository.events)
        self.repository.clear_events()
        delattr(self, '_repository')

    @t.final
    def _post_rollback(self):
        """Очищаем текущие события репозитория"""
        if hasattr(self, '_repository'):
            self.repository.clear_events()
            delattr(self, '_repository')

    def __enter__(self):
        if self._in_context:
            raise RuntimeError("Double enter to UnitOfWork's context manager")
        self._repository = self._repository_class(self._connection)
        self._current_transaction_events.clear()
        self._in_context = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._events.update(self._current_transaction_events)
        self._current_transaction_events.clear()
        self._in_context = False


class AbstractAsyncUnitOfWork(AbstractUnitOfWork[R, T]):

    @t.final
    async def __aenter__(self):
        self._current_transaction_events.clear()
        self._connection = await self._begin_transaction(self._engine)
        self.__enter__()

    @t.final
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        self.__exit__(exc_type, exc_val, exc_tb)

    @t.final
    async def commit(self):
        await self.repository.apply_changes()
        await self._commit_transaction(self._connection)
        self._post_commit()

    @t.final
    async def rollback(self):
        await self._rollback_transaction(self._connection)
        self._post_rollback()

    @abc.abstractmethod
    async def _begin_transaction(self, factory: t.Any) -> T:
        ...

    @abc.abstractmethod
    async def _commit_transaction(self, connection: T):
        ...

    @abc.abstractmethod
    async def _rollback_transaction(self, connection: T):
        ...


class AbstractSyncUnitOfWork(AbstractUnitOfWork[R, T]):

    @t.final
    def __enter__(self):
        self._connection = self._begin_transaction(self._engine)
        super(AbstractSyncUnitOfWork, self).__enter__()

    @t.final
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()
        super(AbstractSyncUnitOfWork, self).__exit__(exc_type, exc_val, exc_tb)

    @t.final
    def commit(self):
        self.repository.apply_changes()
        self._commit_transaction(self._connection)
        self._post_commit()

    @t.final
    def rollback(self):
        self._rollback_transaction(self._connection)
        self._post_rollback()

    @abc.abstractmethod
    def _begin_transaction(self, factory: t.Any) -> T:
        ...

    @abc.abstractmethod
    def _commit_transaction(self, connection: T):
        ...

    @abc.abstractmethod
    def _rollback_transaction(self, connection: T):
        ...

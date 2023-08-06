import abc
import logging
import typing as t
from asyncio import AbstractEventLoop
from collections import defaultdict
from inspect import isclass

from dddmisc import DDDCommand, DDDEvent, AbstractAsyncUnitOfWork, DDDResponse, AbstractSyncUnitOfWork, \
    AbstractSyncRepository, AbstractAsyncRepository
from dddmisc.aggregate import BaseAggregate

__all__ = ['AbstractSyncExternalMessageBus', 'AbstractAsyncExternalMessageBus', 'EventHandlerType',
           'CommandHandlerType']

AsyncEventHandlerType = t.Callable[[DDDEvent, AbstractAsyncUnitOfWork], t.Awaitable]
AsyncCommandHandlerType = t.Callable[[DDDCommand, AbstractAsyncUnitOfWork], t.Awaitable[BaseAggregate]]
SyncEventHandlerType = t.Callable[[DDDEvent, AbstractSyncUnitOfWork], t.Any]
SyncCommandHandlerType = t.Callable[[DDDCommand, AbstractSyncUnitOfWork], BaseAggregate]
EventHandlerType = t.Union[SyncEventHandlerType, AsyncEventHandlerType]
CommandHandlerType = t.Union[SyncCommandHandlerType, AsyncCommandHandlerType]


class AbstractAsyncExternalMessageBus(abc.ABC):
    _loop: AbstractEventLoop

    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    def set_loop(self, loop: AbstractEventLoop):
        if not hasattr(self, '_loop'):
            self._loop = loop
        else:
            raise RuntimeError('loop is already set')

    @t.overload
    async def handle(self, message: DDDCommand, timeout: float = None) -> DDDResponse:
        ...

    @t.overload
    async def handle(self, message: DDDEvent, timeout: float = None) -> t.NoReturn:
        ...

    @abc.abstractmethod
    async def handle(self, message, timeout=None):
        ...

    @abc.abstractmethod
    async def start(self):
        ...

    @abc.abstractmethod
    async def stop(self, exception: Exception = None):
        ...


class AbstractSyncExternalMessageBus(abc.ABC):

    @t.overload
    def handle(self, message: DDDCommand, timeout: float = None) -> DDDResponse: ...

    @t.overload
    def handle(self, message: DDDEvent, timeout: float = None) -> t.NoReturn: ...

    @abc.abstractmethod
    def handle(self, message, timeout=None):
        ...

    @abc.abstractmethod
    def start(self):
        ...

    @abc.abstractmethod
    def stop(self, exception: Exception = None):
        ...


EH = t.TypeVar('EH', bound=t.Union[SyncEventHandlerType, AsyncEventHandlerType])
CH = t.TypeVar('CH', bound=t.Union[SyncCommandHandlerType, AsyncCommandHandlerType])
UOW = t.TypeVar('UOW', bound=t.Union[AbstractSyncUnitOfWork, AbstractAsyncUnitOfWork])
R = t.TypeVar('R', bound=t.Union[AbstractSyncRepository, AbstractAsyncRepository])


class AbstractInternalMessagebus(abc.ABC, t.Generic[UOW, R, EH, CH]):

    def __init__(self, uow_class: t.Type[UOW], engine, *, repository_class: t.ClassVar[R] = None, logger='ddd-misc'):
        self._uow_class = uow_class
        self._engine = engine
        self._repository_class = repository_class
        self._EVENT_HANDLERS: t.Dict[t.Type[DDDEvent], t.Set[EH]] = defaultdict(set)
        self._COMMAND_HANDLERS: t.Dict[t.Type[DDDCommand], CH] = {}
        self._logger = logger if isinstance(logger, logging.Logger) else logging.getLogger(logger)

    @t.overload
    def register(self, message: t.Type[DDDEvent], handler: EH):
        ...

    @t.overload
    def register(self, message: t.Type[DDDCommand], handler: CH):
        ...

    def register(self, message, handler):
        if not isclass(message):
            message = type(message)
        if issubclass(message, DDDEvent):
            self._EVENT_HANDLERS[message].add(handler)
        elif issubclass(message, DDDCommand):
            self._COMMAND_HANDLERS[message] = handler
        else:
            raise TypeError(f'message can be subclass or instance of DDDEvent or DDDCommand, not {message!r}')

    @t.overload
    def get_handlers(self, message: t.Union[DDDEvent, t.Type[DDDEvent]]) -> t.Tuple[EH]:
        ...

    @t.overload
    def get_handlers(self, message: t.Union[DDDCommand, t.Type[DDDCommand]]) -> CH:
        ...

    def get_handlers(self, message):
        if not isclass(message):
            message = type(message)
        if issubclass(message, DDDEvent):
            result = tuple(self._EVENT_HANDLERS.get(message, ()))
        elif issubclass(message, DDDCommand):
            result = self._COMMAND_HANDLERS.get(message, None)
        else:
            raise TypeError(f'message can be subclass or instance of DDDEvent or DDDCommand, not {message!r}')
        if result is None:
            raise RuntimeError(f'Not found registered handlers for {message!r}')
        else:
            return result

    def get_uow(self) -> UOW:
        return self._uow_class(self._engine, repository_class=self._repository_class)

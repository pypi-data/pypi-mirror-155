import asyncio
import threading
import typing as t
from queue import Queue, Empty

from tenacity import Retrying, stop_after_attempt, RetryError, wait_exponential, AsyncRetrying

from dddmisc import DDDEvent, AbstractSyncUnitOfWork, AbstractSyncRepository, DDDCommand, DDDResponse, \
    AbstractAsyncUnitOfWork, AbstractAsyncRepository
from dddmisc.messagebus.abstract import SyncEventHandlerType, AbstractInternalMessagebus, SyncCommandHandlerType, \
    AsyncEventHandlerType, AsyncCommandHandlerType


class EventHandlersExecutor(threading.Thread):

    def __init__(self, messagebus: AbstractInternalMessagebus, logger, event_retrying):
        self.events_queue = Queue()
        self.messagebus = messagebus
        self._run_flag = True
        self._event_retrying = event_retrying
        self._logger = logger
        super(EventHandlersExecutor, self).__init__(daemon=True)

    def run(self) -> None:
        is_empty = False
        while self._run_flag or not is_empty:
            try:
                event = self.events_queue.get(timeout=0.001)
                is_empty = False
                self._handle_event(event)
            except Empty:
                is_empty = True
            else:
                self.events_queue.task_done()

    def stop(self, exception=None):
        self._run_flag = False
        # self.events_queue.join()
        self.join()

    def thread_safe_handle_event(self, event: DDDEvent):
        if self._run_flag:
            self.events_queue.put(event)

    def _handle_event(self, event: DDDEvent): # TODO разобраться с многопоточным запуском
        for handler in self.messagebus.get_handlers(event):
            try:
                for attempt in Retrying(stop=stop_after_attempt(self._event_retrying),
                                        wait=wait_exponential(min=1, max=15)):
                    with attempt:
                        uow = self.messagebus.get_uow()
                        handler(event, uow)
                        for ev in uow.collect_events():
                            self.events_queue.put(ev)
            except RetryError as retry_failure:
                self._logger.exception(
                    'Failure publish event %s to handler %s (attempts count %s)',
                    event, handler, retry_failure.last_attempt.attempt_number
                )


class MessageBus(AbstractInternalMessagebus[
                     AbstractSyncUnitOfWork, AbstractSyncRepository, SyncEventHandlerType, SyncCommandHandlerType]):

    def __init__(self, uow_class, engine, *, repository_class=None,
                 event_retrying: int = 5, logger='ddd-misc'):
        super(MessageBus, self).__init__(uow_class, engine, repository_class=repository_class, logger=logger)
        self._event_executor = EventHandlersExecutor(self, self._logger, event_retrying)

    def start(self):
        self._event_executor.start()

    def stop(self, exception: Exception = None):
        self._event_executor.stop(exception)

    @t.overload
    def handle(self, message: DDDEvent) -> t.NoReturn:
        ...

    @t.overload
    def handle(self, message: DDDCommand) -> DDDResponse:
        ...

    def handle(self, message):
        if isinstance(message, DDDCommand):
            return self._handle_command(message)
        elif isinstance(message, DDDEvent):
            self._event_executor.thread_safe_handle_event(message)
        else:
            self._logger.error('Handle not valid message type %s in messagebus %s', message, self)
            raise TypeError(f'{message} was not and DDDEvent ot DDDCommand')

    def _handle_command(self, command: DDDCommand) -> DDDResponse:
        handler = self.get_handlers(command)
        try:
            uow = self.get_uow()
            response = handler(command, uow)
            result = DDDResponse(command.__reference__, response)
            for event in uow.collect_events():
                self._event_executor.thread_safe_handle_event(event)
            return result
        except:
            self._logger.exception('Failure publish command %s to handler %s', command, handler)
            raise


class AsyncMessageBus(AbstractInternalMessagebus[AbstractAsyncUnitOfWork, AbstractAsyncRepository,
                                                 AsyncEventHandlerType, AsyncCommandHandlerType]):
    _loop: asyncio.AbstractEventLoop

    def __init__(self, uow_class, engine, *, repository_class=None,
                 event_retrying: int = 5, logger='ddd-misc'):
        self._tasks: t.Set[asyncio.Task] = set()
        self._is_run = False
        self._daemon_task: asyncio.Task = None
        self._start_event: asyncio.Event = None

        self._event_retrying: int = event_retrying
        super(AsyncMessageBus, self).__init__(uow_class, engine, repository_class=repository_class, logger=logger)

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    @property
    def loop(self):
        return self._loop

    async def start(self):
        self._start_event = asyncio.Event(loop=self.loop)
        self._daemon_task = self.loop.create_task(self._run_daemon())
        await self._start_event.wait()

    async def stop(self, exception: Exception = None):
        self._start_event.clear()
        if self._daemon_task and not self._daemon_task.done():
            await self._daemon_task
        while self._tasks:
            tasks = tuple(self._tasks)
            await asyncio.gather(*tasks, return_exceptions=True)
            self._tasks.difference_update(tasks)

    async def _run_daemon(self):
        self._start_event.set()
        while self._start_event.is_set():
            if self._tasks:
                done, pending = await asyncio.wait(self._tasks, timeout=0.001)
                self._tasks.difference_update(done)
            else:
                await asyncio.sleep(0.001)

    @t.overload
    async def handle(self, message: DDDEvent):
        ...

    @t.overload
    async def handle(self, message: DDDCommand) -> DDDResponse:
        ...

    async def handle(self, message):
        if isinstance(message, DDDCommand):
            return await self._handle_command(message)
        elif isinstance(message, DDDEvent):
            return self._handle_event(message)
        else:
            self._logger.error('Handle not valid message type %s in messagebus %s', message, self)
            raise TypeError(f'{message} was not and DDDEvent ot DDDCommand')

    async def _handle_command(self, command: DDDCommand):
        handler = self.get_handlers(command)
        try:
            uow = self.get_uow()
            response = await handler(command, uow)
            result = DDDResponse(command.__reference__, response)
            for event in uow.collect_events():
                self._handle_event(event)
            return result
        except:
            self._logger.exception('Failure publish command %s to handler %s', command, handler)
            raise

    def _handle_event(self, event: DDDEvent):
        for handler in self.get_handlers(event):
            task = self.loop.create_task(self._execute_handler_event(handler, event))
            self._tasks.add(task)

    async def _execute_handler_event(self, handler: AsyncEventHandlerType, event: DDDEvent):
        try:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(self._event_retrying),
                                               wait=wait_exponential(min=1, max=15)):
                with attempt:
                    uow = self.get_uow()
                    await handler(event, uow)
                    for ev in uow.collect_events():
                        self._handle_event(ev)
        except RetryError as retry_failure:
            self._logger.exception(
                'Failure publish event %s to handler %s (attempts count %s)',
                event, handler, retry_failure.last_attempt.attempt_number
            )

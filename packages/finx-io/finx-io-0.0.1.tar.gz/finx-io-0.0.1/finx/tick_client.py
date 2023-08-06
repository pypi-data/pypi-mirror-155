import asyncio
import functools
import json
import websockets

from typing import Callable, Coroutine, List, Union


def ws_endpoint(environment: str = None):
    if environment == 'dev':
        return 'ws://54.152.2.221:3000'
    return 'ws://ws.finx.io'


def task_runner(task: Coroutine):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    run_loop = (loop.is_running() and loop.create_task) or loop.run_until_complete
    try:
        return run_loop(task)
    except TypeError:
        raise Exception('BAD LOOP PARAMS')


class Hybrid:

    def __init__(self, func: Callable):
        self._func = func
        self._func_name = func.__name__
        self._func_path = func.__name__
        self._func_class = None
        functools.update_wrapper(self, func)

    def __get__(self, obj, objtype):
        """Support instance methods."""
        self._func_class = obj
        return self

    def __call__(self, *args, **kwargs):
        return task_runner(self.run_func(*args, **kwargs))

    async def run_func(self, *args, **kwargs):
        if self._func_class is not None:
            args = (self._func_class,) + args
        return await self._func(*args, **kwargs)

    async def run_async(self, *args, **kwargs):
        return await self.run_func(*args, **kwargs)


class TickPlant:

    def __init__(self, api_key: str, environment: str = "dev"):
        self.api_key = api_key
        self.endpoint = ws_endpoint(environment)

    async def __aenter__(self):
        self._conn = websockets.connect(self.endpoint)
        self.websocket = await self._conn.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def __send(self, message: dict):
        message.update(APIKey=self.api_key)
        await self.websocket.send(json.dumps(message))

    async def __receive(self):
        return await self.websocket.recv()

    async def _dispatch(self, message: dict):
        await self.__send(message)
        return await self.__receive()

    async def get_reference_data(self, ticker: str) -> dict:
        return await self._dispatch(dict(securityId=ticker, functionName='referenceData'))

    async def tick_snap(self, pair: str, date: str, time: str = "00:00") -> dict:
        return await self._dispatch(dict(
            pair=pair,
            date=date,
            time=time,
            functionName='tickSnap'))

    async def tick_history(self, pair: str, date: str, time: str = "00:00") -> dict:
        return await self._dispatch(dict(
            pair=pair,
            date=date,
            time=time,
            functionName='tickHistory'))

    @Hybrid
    async def connect(self):
        await self.__aenter__()

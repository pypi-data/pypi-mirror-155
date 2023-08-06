from __future__ import annotations

from typing import TYPE_CHECKING, Any, Coroutine

import aioredis
from asgiref.sync import async_to_sync

from .exceptions import BadRequest, NotAuthorized, NotFound
from .sessions import sessions


# async def reflect(*args, **kwargs) -> Coroutine[Any]:
async def reflect(*args, **kwargs):

    coro = sessions["global"].reflect(*args, **kwargs)

    # loop = asyncio.get_event_loop()
    # return loop.run_until_complete(coro)
    try:
        return await coro
    except aioredis.exceptions.RedisError as e:
        print(e)


reflect_sync = async_to_sync(reflect)

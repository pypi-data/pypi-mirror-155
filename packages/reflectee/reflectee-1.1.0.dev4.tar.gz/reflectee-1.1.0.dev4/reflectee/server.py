from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any, Coroutine

import socketio
from asgiref.sync import async_to_sync

from .core.sessions import sessions
from .utils import import_class

__all__ = [
    "create_asgi_app",
    "sio",
    "Session",
    "Event",
    "Resolver",
    "reflect",
]


REDIS_URL = os.environ.get("REFLECTEE_REDIS_URL", "")
JSON_ENCODER = os.environ.get("REFLECTEE_JSON_ENCODER", "reflectee.JSONEncoder")
SESSION_CLASS = os.environ.get(
    "REFLECTEE_SESSION_CLASS", "reflectee.core.session.Session"
)
Session = import_class(SESSION_CLASS)
sio: socketio.AsyncServer = None
# Session = None
Event = Session.EventClass
reflect = None
global_session = None

if REDIS_URL:
    mgr: socketio.AsyncRedisManager = socketio.AsyncRedisManager(REDIS_URL)
else:
    mgr = None

sio = socketio.AsyncServer(
    # aiohttp
    # asgi
    async_mode="asgi",
    client_manager=mgr,
    cors_allowed_origins="*",
    # engineio_logger=False,
    # logger=settings.DEBUG,
)

try:
    Event = Session.EventClass
    from .core.reflect import reflect
except ImportError:
    pass  # skip circular import second pass

JSONEncoder = import_class(JSON_ENCODER)
json.JSONEncoder = JSONEncoder


def create_asgi_app(app=None):

    sessions["global"] = Session(sio, "global", {}, {})

    @sio.event
    async def connect(sid, environ, auth):
        sessions[sid] = Session(sio, sid, environ, auth)
        await sessions[sid].connect()

    @sio.event
    async def disconnect(sid):
        # async def disconnect(sid):
        await sessions[sid].close()
        del sessions[sid]

    @sio.on("*")
    async def catch_all(event, sid, data):
        return await sessions[sid].on(event, data)

    return socketio.ASGIApp(sio, app)


# @sio.on('connection-bind')
# async def connection_bind(sid, data):
#                // code to capture the data
#    // sid is a unique id for each connection and data contains additional payload of the message.

# @sio.on('disconnect')
# async def test_disconnect(sid):
#     // code to capture the data
#    // sid is a unique id for each connection and data contains additional payload of the message.

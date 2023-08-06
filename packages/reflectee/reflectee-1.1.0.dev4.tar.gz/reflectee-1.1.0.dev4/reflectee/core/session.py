from __future__ import annotations

import inspect
import traceback
from typing import TYPE_CHECKING, Any, Coroutine

from .event import Event
from .exceptions import RequestException, UnexpectedError
from .handlers import handlers
from .reflect import reflect
from .serializers import Input as InputModel
from .serializers import Output as OutputModel

if TYPE_CHECKING:
    from socketio import AsyncServer

__all__ = ["Session"]


class User:
    sid: str


class Session(object):

    UserClass: User = User
    EventClass: Event = Event
    sid = None

    def __init__(self, sio: AsyncServer, sid: str, environ, auth):

        self.sio: AsyncServer = sio
        self.sid: str = sid
        self.UserClass = self.get_user_class()
        self.user = None
        self.environ = environ
        self.auth = auth
        self.event: str = None
        self.debug: bool = self.get_debug()
        self.EventClass = self.get_event_class()

    async def connect(self):
        await self.set_user(self.get_default_user())

    # attach user the socket session (sid)
    async def set_user(self, user) -> Coroutine[object]:
        # print("JOIN", self.get_user_room(user))
        await self.join(self.get_user_room(user))
        # set user on session
        self.user = user

    def get_default_user(self):
        return self.get_user_class()

    def get_user_class(self):
        return self.UserClass

    def get_event_class(self):
        return self.EventClass

    def get_debug(self):
        return False

    # get the room name for an user
    def get_user_room(self, user):
        return f"user.{user}"

    # join a shared room
    async def join(self, channel):
        self.sio.enter_room(self.sid, channel)

    # leave a shared room
    async def leave(self, channel):
        self.sio.leave_room(self.sid, channel)

    async def resolve_to(self, to):
        if isinstance(to, str):
            return to
        elif isinstance(to, self.UserClass):
            return self.get_user_room(to)
        else:
            return self.sid

    async def resolve_error(self, *args, **kwargs):
        await self.sio.emit(*args, **kwargs, to=self.sid, ignore_queue=True)

    # on new message from client, got event and input data
    async def on(self, handler, input):

        try:
            handler_id: list = handler.rsplit("#", 1)
            handler: str = handler_id[0]
            id: str = handler_id[1] if len(handler_id) > 1 else None
            event: self.Event = self.EventClass(
                self, handler=handler, input=input, id=id
            )
            callback_value = await event.call(handlers)
            if callback_value:
                # event.reflect(callback_value, resolve=True, skip=self.sid)
                return callback_value

        except RequestException as e:
            if self.debug:
                print(traceback.format_exc())
                await self.resolve_error(
                    dict(
                        event=handler,
                        input=input,
                        error=str(e),
                        traceback=traceback.format_exc(),
                    )
                )
            return dict(error=str(e))

        except Exception as e:
            if self.debug:
                print(traceback.format_exc())
                await self.resolve_error(
                    dict(
                        event=handler,
                        input=input,
                        error=str(e),
                        traceback=traceback.format_exc(),
                    )
                )
                return dict(
                    error=str(e),
                    traceback=traceback.format_exc(),
                )
            else:
                # TODO: log error
                return dict(event=handler, error="Unexpected error")

    def serialize_input(self, Model: InputModel, data):
        if isinstance(data, dict):
            return Model(**data)
        elif isinstance(data, str):
            return data
        else:
            return data

    def serialize_output(self, Model: OutputModel, obj):

        # TODO: check type is dictor omething
        return Model(**obj)

    # dispatch message to any kind of
    async def reflect(
        self,
        event: str,
        data: Any,
        to=None,
        # to_as_user_id=False,
        id=None,
        resolve: bool = False,
        broadcast: bool = False,
        skip_sid=None,
        skip_me=None,
    ) -> Coroutine[Any]:

        if id:
            event = f"{event}#{id}"

        if resolve:
            ignore_queue = True
        else:
            ignore_queue = False

        if broadcast:
            to = None
        else:
            to = await self.resolve_to(to)

        await self.sio.emit(
            event, data, to=to, ignore_queue=ignore_queue, skip_sid=skip_sid
        )
        # TODO: return something that can change the ID
        return data

        # return await reflect(*args, **kwargs, session=self)

    async def close(self):
        pass

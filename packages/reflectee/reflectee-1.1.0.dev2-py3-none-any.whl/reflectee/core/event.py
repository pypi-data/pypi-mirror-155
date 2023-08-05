from __future__ import annotations

from typing import TYPE_CHECKING, Any, Coroutine

if TYPE_CHECKING:
    from .session import Session

from .exceptions import BadRequest, NotAuthorized, NotFound

__all__ = ["Event"]


class Event:

    BadRequest = BadRequest
    NotFound = NotFound
    NotAuthorized = NotAuthorized

    def __init__(
        self,
        session: Session,
        handler: str,
        input: Any = None,
        id: str | None = None,
    ):
        self.session: Session = session
        self.handler: str = handler
        self.id: str | None = id
        self.data: Any = input

    @property
    def user(self):
        return self.session.user

    @property
    def User(self):
        return self.session.User

    async def set_user(self, *args, **kwargs) -> Coroutine[Any]:
        await self.session.set_user(*args, **kwargs)

    async def call(self, handlers):
        if self.handler in handlers:
            return await handlers[self.handler](self)
        else:
            raise self.BadRequest(f"handler {self.handler} not found")

    # dispatch message to any kind of
    async def reflect(
        self,
        data: Any,
        event: str = None,
        id=None,
        skip_self=False,
        skip_sid=None,
        **kwargs,
    ) -> Coroutine[Any]:

        if not isinstance(event, str):
            event = self.handler
        # TODO: verify the handlers existence

        if not isinstance(id, (str, int)):
            id = self.id

        if skip_self:
            skip_sid = self.session.sid

        if id != self.id and skip_sid == self.session.sid:
            raise Exception(
                "id cannot be different than to previous one for callbacks (skip self)"
            )

        return await self.session.reflect(
            event,
            data,
            id=id,
            skip_sid=skip_sid,
            **kwargs,
        )

    async def reflect_to(self, data, to, *args, **kwargs):
        kwargs["to"] = to
        kwargs["skip_self"] = True
        return await self.reflect(data, *args, **kwargs)

    async def reflect_to_me(self, data, *args, **kwargs):
        kwargs["to"] = self.user
        kwargs["skip_self"] = True
        return await self.reflect(data, *args, **kwargs)

    # emit message to all user in session via rooms
    async def broadcast(self, *args, **kwargs) -> Coroutine[Any]:
        return await self.reflect(*args, **kwargs, broadcast=True)

    # async def resolve(self, *args, **kwargs) -> Coroutine[Any]:
    #     # Return the data for direct socket callback and ignore self SID for other dispatching
    #     # usefull for exemple to broacast something at the end of handler and send the callback int a fastest way to the user
    #     # return await event.resolve({ ...something... }, broadcast=True)
    #     return await self.reflect(
    #         *args, **kwargs, resolve=True, skip=self.session.sid
    #     )

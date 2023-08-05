from __future__ import annotations

from typing import TYPE_CHECKING, Any, Coroutine

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from ..core.event import Event as BaseEvent

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    from .session import Session

    # User = get_user_model()

__all__ = ["Event"]


class Event(BaseEvent):
    def __init__(self, session: Session, *args, **kwargs):
        super().__init__(session, *args, **kwargs)

    async def call(self, *args, **kwargs):
        try:
            return await super().call(*args, **kwargs)
        except ObjectDoesNotExist as e:
            raise self.NotFound(e)

    async def reflect_staff(self, *args, **kwargs) -> Coroutine[Any]:
        return await self.reflect(*args, **kwargs, to="users.staff")

    async def reflect_admin(self, *args, **kwargs) -> Coroutine[Any]:
        return await self.reflect(*args, **kwargs, to="users.admin")

    async def reflect_superadmin(self, *args, **kwargs) -> Coroutine[Any]:
        return await self.reflect(*args, **kwargs, to="users.superadmin")

    async def set_user(self, *args, **kwargs) -> Coroutine[User]:
        await super().set_user(*args, **kwargs)

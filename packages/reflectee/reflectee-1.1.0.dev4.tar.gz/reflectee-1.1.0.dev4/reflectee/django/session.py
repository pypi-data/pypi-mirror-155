from __future__ import annotations

from itertools import chain
from typing import TYPE_CHECKING, Coroutine

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.fields.related import RelatedField
from django.forms.models import model_to_dict

from ..core.serializers import Output as OutputModel
from ..core.session import Session as SessionBase
from .event import Event

if TYPE_CHECKING:
    from django.contrib.auth.models import User

    # User = get_user_model()

__all__ = ["Session"]


class Session(SessionBase):

    UserClass: User = None
    EventClass: Event = Event

    # attach user the socket session (sid)
    async def set_user(self, user, **kwargs) -> Coroutine[User]:

        # if user exist and already connected to an other user room (few chance.. but for hacking safety)

        if getattr(self.user, "pk", None) and getattr(
            self.user, "pk", None
        ) != getattr(user, "pk", None):
            await self.leave(self.get_user_room(self.user))
        # if user exist and real, join his own private room

        if getattr(user, "pk", None):
            await self.join(self.get_user_room(user))

        if hasattr(user, "is_staff"):
            if user.is_staff is True:
                await self.join("users.staff")

        if hasattr(user, "is_active"):
            if user.is_active is True:
                await self.join("users.active")
            else:
                await self.join("users.inactive")

        if hasattr(user, "is_admin"):
            if user.is_admin is True:
                await self.join("users.admin")

        if hasattr(user, "is_superuser"):
            if user.is_superuser is True:
                await self.join("users.superuser")

        await super().set_user(user, **kwargs)

    def get_user_room(self, user):
        return f"user.{user.pk}"

    def get_user_class(self):
        if not self.UserClass:
            return get_user_model()
        else:
            return self.UserClass

    def get_debug(self):
        return settings.DEBUG

    def serialize_input(self, *args, **kwargs):
        return super().serialize_input(*args, **kwargs)

    def serialize_output(
        self, Model: OutputModel, instance, fields=None, exclude=None
    ):

        # TODO: check type is dict or django model

        opts = instance._meta
        # data = {}

        data = model_to_dict(instance)

        print("FOR DJANGO", OutputModel.__fields__)
        # for name, field in OutputModel.__fields__

        #     print(name, field)

        # if issubclass(field.__class__, RelatedField)

        # RelatedField

        # for f in chain(
        #     opts.concrete_fields, opts.private_fields, opts.many_to_many
        # ):
        #     if not getattr(f, "editable", False):
        #         continue
        #     if fields is not None and f.name not in fields:
        #         continue
        #     if exclude and f.name in exclude:
        #         continue
        #     data[f.name] = f.value_from_object(instance)

        data["id"] = instance.pk
        print(data)
        # return dict(output.from_orm(obj))
        return Model(**data)

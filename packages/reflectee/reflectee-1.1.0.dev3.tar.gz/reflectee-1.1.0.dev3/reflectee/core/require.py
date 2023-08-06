from pydantic import BaseModel, ValidationError, validator

from ..utils import camelcase
from . import exceptions

__all__ = ["require"]


class Require:
    def __init__(self):
        pass

    def user(
        self,
        is_authenticated=None,
        is_verified=None,
        is_anonymous=None,
        is_superadmin=None,
        is_admin=None,
        is_staff=None,
        perms=None,
    ):
        def wrapper(handle):
            async def new_handle(event, **kwargs):

                if is_authenticated is not None:
                    if is_authenticated != event.user.is_authenticated:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if is_anonymous is not None:
                    if is_anonymous != event.user.is_anonymous:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if is_verified is not None:
                    if is_verified != event.user.is_verified:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if is_staff is not None:
                    if is_staff != event.user.is_staff:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if is_admin is not None:
                    if is_admin != event.user.is_admin:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if is_superadmin is not None:
                    if is_superadmin != event.user.is_superadmin:
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )

                if perms is not None:
                    if not set(perms).intersection(event.user.perms):
                        raise exceptions.NotAuthorized(
                            "insufficient permissions"
                        )
                return await handle(event, **kwargs)

            return new_handle

        return wrapper


require = Require()

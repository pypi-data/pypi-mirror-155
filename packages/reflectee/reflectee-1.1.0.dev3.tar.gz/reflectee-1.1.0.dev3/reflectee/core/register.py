import inspect

from pydantic import ValidationError

from . import exceptions
from .handlers import API_PATH, _register

__all__ = ["register"]


def register(event: str | None = None, input=None, output=None, user=None):
    def wrapper(original_handle):

        # Wrapp handler
        async def real_handler(event, **kwargs):

            # TODO: check input is pydantic Based Model
            if input:
                try:
                    kwargs["input"] = event.session.serialize_input(
                        input, event.data
                    )
                except ValidationError as e:
                    raise exceptions.BadRequest(e)

            # TODO: check output is pydantic Based Model
            if output:
                try:
                    kwargs[
                        "output"
                    ] = lambda *args, **kwargs: event.session.serialize_output(
                        output, *args, **kwargs
                    )
                except ValidationError as e:
                    raise exceptions.BadRequest(e)

            # TODO: check is method
            if user:
                #  event.session.require_user()
                pass

            return await original_handle(event, **kwargs)

        # Register event
        if not event:
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            filename = module.__file__
            event2 = str(filename).split(API_PATH, 1)[-1][:-3].strip("/")
            _register(event2, real_handler)
        else:
            _register(event, real_handler)

        return real_handler

    return wrapper

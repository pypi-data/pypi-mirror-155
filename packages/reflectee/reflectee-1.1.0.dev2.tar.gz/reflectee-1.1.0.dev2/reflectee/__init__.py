import os

from . import utils
from .core import exceptions, serializers
from .core.encoder import JSONEncoder
from .core.reflect import reflect, reflect_sync
from .core.register import register
from .core.require import require
from .utils import import_class
from .utils.pagination import paginate

SESSION_CLASS = os.environ.get(
    "REFLECTEE_SESSION_CLASS", "reflectee.core.session.Session"
)
Session = import_class(SESSION_CLASS)
Event = Session.EventClass

__all__ = [
    "require",
    "serializers",
    "exceptions",
    "register",
    "paginate",
    "utils",
    "JSONEncoder",
    # From server dynhamics
    "Session",
    "Event",
    "reflect",
    "reflect_sync",
]
# , "django_asgi_app"]
# , "django_wsgi_app"]
# , "flask_asgi_app"]
# , "flask_wsgi_app"]
# , "fastapi_asgi_app"]
# , "fastapi_wsgi_app"]


# Django shortcut
default_app_config = "reflectee.django.apps.DjangoAppConfig"

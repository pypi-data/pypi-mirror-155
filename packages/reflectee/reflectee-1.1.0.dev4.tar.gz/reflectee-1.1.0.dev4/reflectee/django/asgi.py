import os

import socketio

import django
from django.core.asgi import get_asgi_application

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


django.setup()
from django.conf import settings

os.environ.setdefault(
    "REFLECTEE_REDIS_URL", getattr(settings, "REFLECTEE_REDIS_URL", "")
)

os.environ.setdefault(
    "REFLECTEE_SESSION_CLASS",
    getattr(settings, "REFLECTEE_SESSION_CLASS", "reflectee.django.Session"),
)

from ..server import create_asgi_app

app: socketio.ASGIApp = create_asgi_app(get_asgi_application())

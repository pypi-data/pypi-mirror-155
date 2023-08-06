import json
from datetime import date, datetime
from typing import Iterable
from uuid import UUID

__all__ = ["JSONEncoder"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, Iterable):
            return list(o)
        else:
            return super().default(o)

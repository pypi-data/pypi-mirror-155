# Reflectee :: API ASM

Python async API "**A**s **S**tate **M**anager" for [reflectee.app](http://reflectee.app) apps

## Install

```bash
pip install reflectee
# or
pipenv install reflectee
```

## Django integration

-   Follow the minimal django project's setup : https://www.djangoproject.com/start/<br>

    > An create-app CLI is being developed soon

-   Add the asgi app file

```python
# your_project/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

from reflectee.django.asgi import app
```

-   Add somes into your settings

```python
# your_project/settings.py
INSTALLED_APPS = [
    # ...
    "reflectee",
    # ...
]
# ...
ASGI_APPLICATION = "your_project.asgi"
REFLECTEE_REDIS_URL = REDIS_URL
REFLECTEE_API_PATH = "your_project/api"
# ...
```

-   Then create your first API ASM handler

```python
# your_project/api/hello.py
from reflectee import Event

async def handle(event: Event) -> str:
    await event.reflect('hello client!')
```

-   At this point, use your own asgi server, an ready to production example with daphne :

```bash
pip install --user daphne
daphne -b 0.0.0.0 -p 8000 your_project.asgi:app
```

> An implementaton of runserver for reflectee developement mode is being developed

```bash
pip install --user watchdog
watchmedo auto-restart -R -p 'your_project/*.py' -- daphne -b 0.0.0.0 -p 8000 your_project.asgi:app
```

-   Then, connect ws://127.0.0.1:8000 with the reflectee client, follow the next steps on the npm package README.md

## Typing

```python
# your_project/api/book/comment.py
from reflectee import Event, require

class Author(require.InputData):
    name: str
    age: int | None

class Book(require.InputData):
    title: str
    author: Author

@require.data(input=Book)
async def handle(event: Event, input: Book) -> str:
   return f'{input.title} by {input.author.name} is a great book !'
```

-   Client side

```typescript
import { useReflect } from 'reflectee'

const { data: comment } = useReflect('book/comment', {
    input: {
        title: 'How to use reflectee',
        author: {
            name: 'Dalou',
        },
    },
})
```

## Access control

```python
# your_project/api/admin.py
from reflectee import Event, require

@require.user(is_admin=True)
async def handle(event: Event) -> str:
    return f'{event.user} is an expected admin'
```

-   Client side

```typescript
const { data, error } = useReflect('admin')
console.log(error) // => Permission denied for non-admin
```

<!-- ## React integration

-   Follow the minimal react project's setup : <br>
    Or the nextJS one : <br>

```typescript
// src/main.ts
import { register } from 'reflectee'
register()
```

```typescript
// src/Hello.ts
import { useReflect } from 'reflectee'

export default () => {
    const { data } = useReflect('hello')
    return <p>{data}</p> // <= hello client!
}
``` -->

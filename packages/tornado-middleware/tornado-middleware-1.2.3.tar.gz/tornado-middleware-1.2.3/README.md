# Tornado Middlewares

Middleware support for Tornado Framework

## Install
```bash
pip install tornado-middleware
```

## Example
Create a simple middleware on `RequestHandler` class.

```python
from tornado_middleware import MiddlewareHandler

class IndexHandler(MiddlewareHandler):
    async def middleware_echo(self, next):
        print("Middleware triggered")
        await next()

    def get(self):
        print("Function triggered")
        self.set_status(200)
        self.finish("<html><body><h1>Hello Middleware</h1></body></html>")
```

Create a separately middleware

```python
from tornado_middleware import MiddlewareHandler
from tornado.web import RequestHandler

class EchoMiddleware(MiddlewareHandler):
    async def middleware_echo(self, next):
        print("Middleware triggered")
        await next()

class IndexHandler(EchoMiddleware, RequestHandler):
    def get(self):
        print("Function triggered")
        self.set_status(200)
        self.finish("<html><body><h1>Hello Middleware</h1></body></html>")
```

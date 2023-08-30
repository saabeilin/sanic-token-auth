import typing
from functools import wraps

from sanic import Sanic, exceptions
from sanic.request import Request


class SanicTokenAuth:
    def __init__(
        self,
        app: typing.Optional[Sanic] = None,
        header: typing.Optional[str] = None,
        token_verifier: typing.Optional[typing.Callable] = None,
        secret_key: typing.Optional[str] = None,
    ):
        self.secret_key = secret_key
        self.header = header
        self.token_verifier = token_verifier

    async def _is_authenticated(self, request: Request) -> bool:
        token = request.headers.get(self.header, None) if self.header else request.token
        if self.token_verifier:
            return await self.token_verifier(token)
        return token == self.secret_key

    def auth_required(self, handler=None):
        @wraps(handler)
        async def wrapper(request, *args, **kwargs):
            if not await self._is_authenticated(request):
                raise exceptions.Unauthorized("Auth required.")

            return await handler(request, *args, **kwargs)

        return wrapper

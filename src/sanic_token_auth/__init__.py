from functools import wraps

from sanic import Sanic, exceptions


class SanicTokenAuth:
    def __init__(self, app=None,
                 header=None,
                 token_verifier=None,
                 secret_key=None
                 ):
        self.secret_key = secret_key
        self.header = header
        self.token_verifier = token_verifier
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Sanic):
        """hook on request start etc."""
        app.register_middleware(self.open_session, 'request')

    async def open_session(self, request):
        pass

    async def _is_authenticated(self, request):
        token = request.headers.get(self.header, None) if self.header else request.token
        print(token)
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

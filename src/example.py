import sanic.response
from sanic import Sanic
from sanic.response import text

from sanic_token_auth import SanicTokenAuth

app = Sanic("SanicTokenAuthExample")
auth = SanicTokenAuth(app, secret_key="utee3Quaaxohh1Oo", header="X-My-App-Auth-Token")


@app.route("/")
async def index(request: sanic.Request) -> sanic.response.HTTPResponse:
    return text("Go to /protected")


@app.route("/protected")
@auth.auth_required
async def protected(request: sanic.Request) -> sanic.response.HTTPResponse:
    return text("Welcome!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

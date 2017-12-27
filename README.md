Gotta get your API protected!
=============================

Token-based authentication is the most common way of protecting your APIs from unwanted folk.

Sometimes you need to do things _fast_ (you know, get it to prod _yesterday_) 
and you do not really have time to implement a proper authentication layer.

Okay, are you fine with a temporary solution? There's nothing more permanent than temporary, right.

If you can:

 * provide a simple async token verifier (say, checking it in memcached or Redis)

 or
 * hard-code a token in your app prototype,
 
 and also
 
 * sent the token in a request header
 
 - then we are ready to go.


## Usage example


```python
from sanic import Sanic
from sanic.response import text

from sanic_token_auth import SanicTokenAuth

app = Sanic()
auth = SanicTokenAuth(app, secret_key='utee3Quaaxohh1Oo', header='X-My-App-Auth-Token')


@app.route("/")
async def index(request):
    return text("Go to /protected")


@app.route("/protected")
@auth.auth_required
async def protected(request):
    return text("Welcome!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

And let's try it:

```bash
$ curl http://localhost:8000/protected -H "X-My-App-Auth-Token: utee3Quaaxohh1Oo"

Welcome!
```


If you omit the `header` argument, you can instead send a token in either 
`Authorization: Bearer <yourtoken>` or `Authorization: Token <yourtoken>` 
header.


-----

TODO:

 [ ] Document `token_verifier` and implement examples of using of 
 
 [ ] Implement "protect all" behaviour
 

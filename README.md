# Sanic-SSLify

This is a simple Sanic extension that configures your Sanic application to redirect all incoming requests to HTTPS.

If you're interested in financially supporting Kenneth Reitz open source, consider visiting this link. Your support helps tremendously with sustainability of motivation, as Open Source is no longer part of my day job.

Redirects only occur when app.debug is False.

# Usage

Usage is pretty simple:

from Sanic import Sanic
from sanic_sslify import SSLify

app = Sanic(__name__)
sslify = SSLify(app)
If you make an HTTP request, it will automatically redirect:

$ curl -I http://csdn.net/
HTTP/1.1 301 Moved Permanently
Server: openresty
Date: Tue, 23 Oct 2018 09:07:19 GMT
Content-Type: text/html
Content-Length: 182
Connection: keep-alive
Keep-Alive: timeout=20
Location: https://www.csdn.net/

Sanic-SSLify also provides your application with an HSTS policy.

By default, HSTS is set for one year (31536000 seconds).

You can change the duration by passing the age parameter:

sslify = SSLify(app, age=300)
If you'd like to include subdomains in your HSTS policy, set the subdomains parameter:

sslify = SSLify(app, subdomains=True)
Or by including SSLIFY_SUBDOMAINS in your app's config.

HTTP 301 Redirects

By default, the redirect is issued with a HTTP 302 response. You can change that to a HTTP 301 response by passing the permanent parameter:

sslify = SSLify(app, permanent=True)
Or by including SSLIFY_PERMANENT in your app's config.

Exclude Certain Paths from Being Redirected

You can exlude a path that starts with given string by including a list called skips:

sslify = SSLify(app, skips=['docs', 'auth'])
Or by including SSLIFY_SKIPS in your app's config.

# Install

Installation is simple too:

$ pip install Sanic-SSLify
Security consideration using basic auth

When using basic auth, it is important that the redirect occurs before the user is prompted for credentials. Sanic-SSLify registers a request_middleware handler, to make sure this handler gets executed before credentials are entered it is advisable to not prompt for any authentication inside a response_middleware handler.

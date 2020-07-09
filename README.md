# Sanic-SSLify

This is a simple Sanic extension that configures your Sanic application to redirect all incoming requests to HTTPS.

If you're interested in financially supporting Kenneth Reitz open source, consider visiting this link. Your support helps tremendously with sustainability of motivation, as Open Source is no longer part of my day job.

Redirects only occur when app.debug is False.

# Usage

Usage is pretty simple:
```
from sanic import Sanic
from sanic_sslify import SSLify

app = Sanic(__name__)
sslify = SSLify(app)
```
If you make an HTTP request, it will automatically redirect:
```
$ curl -I http://csdn.net/
HTTP/1.1 301 Moved Permanently
Server: openresty
Date: Tue, 23 Oct 2018 09:07:19 GMT
Content-Type: text/html
Content-Length: 182
Connection: keep-alive
Keep-Alive: timeout=20
Location: https://www.csdn.net/

```
Sanic-SSLify also provides your application with an HSTS policy.

By default, HSTS is set for one year (31536000 seconds).

You can change the duration by passing the age parameter:
```
sslify = SSLify(app, hsts_age=300)
```
Or by including SSLIFY_HSTS_AGE in your app's config.
(But hsts_age parameter if provided will override SSLIFY_HSTS_AGE).

If you'd like to include subdomains in your HSTS policy, set the subdomains parameter:
```
sslify = SSLify(app, hsts_include_subdomains=True)
```
Or by including SSLIFY_HSTS_INCLUDE_SUBDOMAINS in your app's config.
(But hsts_include_subdomains parameter if provided will override SSLIFY_HSTS_INCLUDE_SUBDOMAINS).

HTTP 301 Redirects

By default, the redirect is issued with a HTTP 302 response. You can change that to a HTTP 301 response by passing the permanent parameter:
```
sslify = SSLify(app, permanent_redirect=True)
```
Or by including SSLIFY_PERMANENT_REDIRECT in your app's config.
(But permanent_redirect parameter if provided will override SSLIFY_PERMANENT_REDIRECT).

Exclude Certain Paths from Being Redirected

You can exlude a path that starts with given string by including a list called skips:
```
sslify = SSLify(app, paths_to_skip=['docs', 'auth'])
```
Or by including SSLIFY_PATHS_TO_SKIP in your app's config.
(But paths_to_skip parameter if provided will override SSLIFY_PATHS_TO_SKIP).

# Install

Installation is simple too:

$ pip install Sanic-SSLify
Security consideration using basic auth

When using basic auth, it is important that the redirect occurs before the user is prompted for credentials. Sanic-SSLify registers a request_middleware handler, to make sure this handler gets executed before credentials are entered it is advisable to not prompt for any authentication inside a response_middleware handler.

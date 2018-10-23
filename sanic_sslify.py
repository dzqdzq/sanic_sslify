# -*- coding: utf-8 -*-

from sanic.response import redirect

YEAR_IN_SECS = 31536000


class SSLify(object):
    """Secures your Sanic App."""

    def __init__(self, app, age=YEAR_IN_SECS, subdomains=False, permanent=False, skips=None):
        self.app = app
        self.hsts_age = age

        self.app.config.setdefault('SSLIFY_SUBDOMAINS', False)
        self.app.config.setdefault('SSLIFY_PERMANENT', False)
        self.app.config.setdefault('SSLIFY_SKIPS', None)

        self.hsts_include_subdomains = subdomains or self.app.config['SSLIFY_SUBDOMAINS']
        self.permanent = permanent or self.app.config['SSLIFY_PERMANENT']
        self.skip_list = skips or self.app.config['SSLIFY_SKIPS']

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configures the configured Sanic app to enforce SSL."""
        app.request_middleware.append(self.redirect_to_ssl)
        app.response_middleware.append(self.set_hsts_header)

    @property
    def hsts_header(self):
        """Returns the proper HSTS policy."""
        hsts_policy = 'max-age={0}'.format(self.hsts_age)

        if self.hsts_include_subdomains:
            hsts_policy += '; includeSubDomains'

        return hsts_policy

    def isSkip(self,request):
        """Checks the skip list."""
        # Should we skip?
        if self.skip_list and isinstance(self.skip_list, list):
            for skip in self.skip_list:
                if request.path.startswith('/{0}'.format(skip)):
                    return True
        return False

    def redirect_to_ssl(self,request):
        """Redirect incoming requests to HTTPS."""
        # Should we redirect?
        criteria = [
            request.scheme == 'https',
            self.app.debug,
            request.headers.get('X-Forwarded-Proto', 'http') == 'https'
        ]

        if not any(criteria) and not self.isSkip(request):
            if request.url.startswith('http://'):
                url = request.url.replace('http://', 'https://', 1)
                status = 302
                if self.permanent:
                    status = 301
                r = redirect(url, status=status)
                return r

    def set_hsts_header(self, request,response):
        """Adds HSTS header to each response."""
        # Should we add STS header?
        if not self.isSkip(request):
            response.headers.setdefault('Strict-Transport-Security', self.hsts_header)
        return response

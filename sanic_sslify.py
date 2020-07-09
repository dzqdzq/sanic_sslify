# -*- coding: utf-8 -*-

from sanic.response import redirect

HSTS_YEARS_IN_SECS = 31536000


class SSLify():
    """Secures your Sanic App."""

    def __init__(self, app, hsts_age=HSTS_YEARS_IN_SECS, hsts_include_subdomains=False, permanent_redirection=False, paths_to_skip=[]):
        self.app = app
        self.hsts_age = hsts_age

        self.app.config.setdefault('SSLIFY_HSTS_INCLUDE_SUBDOMAINS', hsts_include_subdomains)
        self.app.config.setdefault('SSLIFY_PERMANENT_REDIRECTION', permanent_redirection)
        self.app.config.setdefault('SSLIFY_PATHS_TO_SKIP', paths_to_skip)

        self.hsts_include_subdomains = self.app.config['SSLIFY_HSTS_INCLUDE_SUBDOMAINS']
        self.permanent_redirection = self.app.config['SSLIFY_PERMANENT_REDIRECTION']
        self.paths_to_skip = self.app.config['SSLIFY_PATHS_TO_SKIP']

        """Configures the configured Sanic app to enforce SSL."""
        app.register_middleware(self.redirect_to_ssl, attach_to='request')
        app.register_middleware(self.set_hsts_header, attach_to='response')

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
        for path_to_skip in self.paths_to_skip:
            if request.path.startswith('/{0}'.format(path_to_skip)):
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
                if self.permanent_redirection:
                    status = 301
                r = redirect(url, status=status)
                return r

    def set_hsts_header(self, request,response):
        """Adds HSTS header to each response."""
        # Should we add STS header?
        if not self.isSkip(request):
            response.headers.setdefault('Strict-Transport-Security', self.hsts_header)
        return response

"""Security for the app."""

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory

from passlib.apps import custom_app_context as pwd_context


class NewRoot(object):
    """Declare New Root object. What pyramid uses to build requests."""

    def __init__(self, request):
        """Take in a http request and builds a request object out of it."""
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'add')
    ]


def check_credentials(username, password):
    """Return True if correct username and password, else False."""
    if username and password:
        # proceed to check credentials
        if username == os.environ["AUTH_USERNAME"]:
            return pwd_context.verify(password, os.environ["AUTH_PASSWORD"])
    return False


def secure_view(request):
    """."""
    check_csrf_token(request)


def includeme(config):
    """Pyramid security configuration."""
    auth_secret = os.environ.get('AUTH_SECRET', 'mongo')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(NewRoot)
    # Session stuff for CSRF Protection
    session_secret = os.environ.get("SESSION_SECRET", "itsaseekrit")
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)

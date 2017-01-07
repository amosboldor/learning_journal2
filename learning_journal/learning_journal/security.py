"""Security for the app."""

import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import check_csrf_token


class NewRoot(object):
    """."""

    def __init__(self, request):
        """."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        # (Allow, Authenticated, 'secret'),
    ]


def check_credentials(username, password):
    """Return True if correct username and password, else False."""
    username = os.environ.get('AUTH_USERNAME', '')
    password = os.environ.get('AUTH_PASSWORD', '')
    if username and password:
        # proceed to check credentials
        if username == os.environ["AUTH_USERNAME"]:
            if password == os.environ["AUTH_PASSWORD"]:
                return True
            # return pwd_context.verify(password, os.environ["AUTH_PASSWORD"])
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
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(NewRoot)
    # # Session stuff for CSRF Protection
    # session_secret = os.environ.get("SESSION_SECRET", "itsaseekrit")
    # config.set_session_factory(session_factory)
    # config.set_default_csrf_options(require_csrf=True)

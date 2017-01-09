"""."""

<<<<<<< HEAD
=======

import os
>>>>>>> b7be6d832a98759f9a0f9ce4e34b32ab9f1db0d2
from pyramid.config import Configurator


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
<<<<<<< HEAD
=======
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]
>>>>>>> b7be6d832a98759f9a0f9ce4e34b32ab9f1db0d2
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    print ('before models')
    config.include('.models')
    print ('before routes')
    config.include('.routes')
    print ('before security')
    config.include('.security')
    print ('before scan')
    config.scan()
    return config.make_wsgi_app()

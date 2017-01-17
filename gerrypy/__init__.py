import os
from pyramid.config import Configurator


def main(global_config, **settings): # pragma: no cover
    """ This function returns a Pyramid WSGI application.
    """
    settings = {'sqlalchemy.url': os.environ["DATABASE_URL"]}
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()

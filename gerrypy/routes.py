def includeme(config):
    config.add_static_view(name='static', path='gerrypy:static')
    config.add_static_view('json', path='gerrypy:views')
    config.add_route('home', '/')
    config.add_route('map', '/map')
    config.add_route('about', '/about')

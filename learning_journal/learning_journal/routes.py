"""Routes for blog pathways."""


def includeme(config):
    """All of the routes for the config."""
    config.add_static_view('static', 'learning_journal:static')
    config.add_route('list', '/')
    config.add_route('create', '/new-entry')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('edit', '/journal/{id:\d+}/edit-entry')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    # config.add_route('forbidden', '/forbidden')
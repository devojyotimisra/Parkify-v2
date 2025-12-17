from application.extensions.cache_extn import cache


def init_cache(app):
    cache.init_app(app)

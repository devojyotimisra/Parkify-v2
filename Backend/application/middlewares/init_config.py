from application.helpers.config import Config


def init_config(app):
    app.config.from_object(Config)

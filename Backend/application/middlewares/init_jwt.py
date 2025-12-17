from application.extensions.jwt_extn import jwt


def init_jwt(app):
    jwt.init_app(app)

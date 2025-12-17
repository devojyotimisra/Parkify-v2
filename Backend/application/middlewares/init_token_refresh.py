from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token


def init_token_refresh(app):
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            verify_jwt_in_request(optional=True)
            identity = get_jwt_identity()
            if identity:
                new_token = create_access_token(identity=identity)
                response.headers['X-Refresh-Token'] = new_token
        except Exception:
            pass
        return response

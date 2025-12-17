from functools import wraps
from flask_jwt_extended import get_jwt_identity
from application.helpers.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        if not user.has_role('admin'):
            return {"error": "Admin access required"}, 403

        return fn(*args, **kwargs)
    return wrapper


def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        if not user.has_role('user'):
            return {"error": "User access required"}, 403

        return fn(*args, **kwargs)
    return wrapper

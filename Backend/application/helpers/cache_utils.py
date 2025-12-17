from flask_jwt_extended import get_jwt_identity


def user_key_prefix():
    user_id = get_jwt_identity()
    return f"user_profile_{user_id}"

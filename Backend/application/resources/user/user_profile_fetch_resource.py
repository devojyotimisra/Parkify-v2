from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.models import User
from application.extensions.cache_extn import cache
from application.helpers.decorators import user_required
from application.helpers.cache_utils import user_key_prefix


class UserProfileFetchResource(Resource):
    @jwt_required()
    @user_required
    @cache.cached(timeout=3600, key_prefix=user_key_prefix)
    def get(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        profile_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "address": user.address,
            "pincode": user.pincode,
            "vehicle_number": user.vehicle_number,
            "active": user.active
        }

        return profile_data, 200

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.models import User
from application.extensions.cache_extn import cache
from application.helpers.decorators import admin_required


class AdminProfileFetchResource(Resource):
    @jwt_required()
    @admin_required
    @cache.cached(timeout=3600, key_prefix="admin_profile_update_key_prefix")
    def get(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "address": user.address,
            "pincode": user.pincode,
            "active": user.active
        }, 200

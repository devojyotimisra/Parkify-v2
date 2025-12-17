from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.models import User, ReserveParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import user_required
from application.extensions.cache_extn import cache


class UserAccountDeleteResource(Resource):
    @jwt_required()
    @user_required
    def delete(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        if not user:
            return {"error": "User not found"}, 404

        if ReserveParkingSpot.query.filter_by(user_id=current_user_id, leaving_timestamp=None).first():
            return {"error": "Cannot delete account while having active reservations"}, 400

        db.session.delete(user)
        db.session.commit()

        cache_key = f"user_profile_{current_user_id}"
        cache.delete(cache_key)

        return {"message": "User account deleted successfully"}, 200

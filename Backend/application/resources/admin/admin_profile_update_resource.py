from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from application.helpers.models import User
from application.extensions.cache_extn import cache
from application.extensions.db_extn import db
from application.helpers.decorators import admin_required
from application.helpers.validators import validate_name, validate_address, validate_pincode, validate_password


class AdminProfileUpdateResource(Resource):
    @jwt_required()
    @admin_required
    def put(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('pincode')
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        if args['name']:
            is_valid, result = validate_name(args['name'])
            if not is_valid:
                return {"error": result}, 400
            user.name = result

        if args['address']:
            is_valid, result = validate_address(args['address'])
            if not is_valid:
                return {"error": result}, 400
            user.address = result

        if args['pincode']:
            is_valid, result = validate_pincode(args['pincode'])
            if not is_valid:
                return {"error": result}, 400
            user.pincode = result

        if args['password']:
            is_valid, result = validate_password(args['password'])
            if not is_valid:
                return {"error": result}, 400
            user.password = generate_password_hash(result)

        db.session.commit()
        cache.delete("admin_profile_update_key_prefix")

        return {"message": "Profile updated successfully"}, 200

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from application.helpers.models import User, Role
from application.extensions.db_extn import db
from application.helpers.validators import validate_email, validate_password, validate_name, validate_address, validate_pincode, validate_vehicle_number
from application.extensions.cache_extn import cache


class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        parser.add_argument('pincode', required=True, help='Pincode is required')
        parser.add_argument('vehicle_number', type=str, required=False)
        args = parser.parse_args()

        is_valid, result = validate_email(args['email'])
        if not is_valid:
            return {"error": result}, 400
        email = result

        is_valid, result = validate_password(args['password'])
        if not is_valid:
            return {"error": result}, 400
        password = result

        is_valid, result = validate_name(args['name'])
        if not is_valid:
            return {"error": result}, 400
        name = result

        is_valid, result = validate_address(args['address'])
        if not is_valid:
            return {"error": result}, 400
        address = result

        is_valid, result = validate_pincode(args['pincode'])
        if not is_valid:
            return {"error": result}, 400
        pincode = result

        is_valid, result = validate_vehicle_number(args['vehicle_number'])
        if not is_valid:
            return {"error": result}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 409

        if result and User.query.filter_by(vehicle_number=result).first():
            return {"error": "Vehicle number already registered"}, 409
        vehicle_number = result

        hashed_password = generate_password_hash(password)

        user_role = Role.query.filter_by(name='user').first()

        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
            db.session.commit()

        new_user = User(
            email=email,
            password=hashed_password,
            name=name,
            address=address,
            pincode=pincode,
            vehicle_number=vehicle_number
        )

        new_user.roles.append(user_role)

        db.session.add(new_user)
        db.session.commit()

        cache_key = f"user_profile_{new_user.id}"
        cache.delete(cache_key)

        access_token = create_access_token(identity=str(new_user.id))

        return {
            "message": "User registered successfully",
            "token": access_token,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name,
                "role": "user"
            }
        }, 201

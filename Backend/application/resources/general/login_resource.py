from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from application.helpers.models import User
from application.helpers.validators import validate_email, validate_password


class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        is_valid, result = validate_email(args['email'])
        if not is_valid:
            return {"error": result}, 400
        email = result

        is_valid, result = validate_password(args['password'])
        if not is_valid:
            return {"error": result}, 400
        password = result

        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "Email not registered"}, 400

        if not check_password_hash(user.password, password):
            return {"error": "Incorrect password"}, 400

        access_token = create_access_token(identity=str(user.id))

        role = 'admin' if user.has_role('admin') else 'user'

        return {
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": role
            }
        }, 200

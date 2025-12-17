from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import User
from application.helpers.decorators import admin_required


class AdminUsersListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        users = User.query.all()
        users_data = []

        for user in users:
            user_roles = [role.name for role in user.roles]

            if 'user' in user_roles:
                users_data.append({
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "address": user.address,
                    "pincode": user.pincode,
                    "vehicle_number": user.vehicle_number,
                    "active": user.active,
                })

        return {"users": users_data}, 200

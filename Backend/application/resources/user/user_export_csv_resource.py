from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.decorators import user_required


class UserExportCSVResource(Resource):
    @jwt_required()
    @user_required
    def get(self):
        current_user_id = int(get_jwt_identity())
        current_app.bg_jobs.export_csv_task.delay(current_user_id)
        return {"message": "Export request received. You will receive an email shortly."}, 202

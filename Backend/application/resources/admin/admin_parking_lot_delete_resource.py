from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot
from application.extensions.db_extn import db
from application.helpers.decorators import admin_required


class AdminParkingLotDeleteResource(Resource):
    @jwt_required()
    @admin_required
    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)

        if not lot:
            return {"error": "Parking lot not found"}, 404

        if lot.occupied_spots_count > 0:
            return {"message": "Cannot delete parking lot with active reservations"}, 400

        db.session.delete(lot)
        db.session.commit()

        return {"message": "Parking lot deleted successfully"}, 200

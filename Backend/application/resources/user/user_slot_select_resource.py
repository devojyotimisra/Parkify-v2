from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot
from application.helpers.decorators import user_required


class UserSlotSelectResource(Resource):
    @jwt_required()
    @user_required
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)

        if not lot:
            return {"error": "Parking lot not found"}, 404

        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

        spots_data = []
        for spot in spots:
            spots_data.append({
                "id": spot.id,
                "lot_id": spot.lot_id,
                "status": spot.status
            })

        return {
            "lot": {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "available_spots_count": lot.available_spots_count
            },
            "spots": spots_data
        }, 200

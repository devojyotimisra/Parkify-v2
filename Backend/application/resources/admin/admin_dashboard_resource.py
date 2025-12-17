from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot
from application.helpers.decorators import admin_required


class AdminDashboardResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        parking_lots = ParkingLot.query.all()

        lots_data = []
        for lot in parking_lots:
            spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
            spots_data = [
                {
                    "id": spot.id,
                    "status": spot.status
                }
                for spot in spots
            ]

            lots_data.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "maximum_number_of_spots": lot.maximum_number_of_spots,
                "available_spots_count": lot.available_spots_count,
                "occupied_spots_count": lot.occupied_spots_count,
                "created_at": lot.created_at.isoformat(),
                "parking_spots": spots_data
            })

        return {"parking_lots": lots_data}, 200

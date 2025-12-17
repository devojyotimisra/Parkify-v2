from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot, ReserveParkingSpot
from application.helpers.decorators import admin_required


class AdminParkingSpotsDetailsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)

        if not lot:
            return {"error": "Parking lot not found"}, 404

        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

        spots_data = []
        for spot in spots:
            spot_info = {
                "id": spot.id,
                "lot_id": spot.lot_id,
                "status": spot.status
            }

            if spot.status == 'O':
                active_reservation = ReserveParkingSpot.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()

                if active_reservation:
                    spot_info["reservation"] = {
                        "id": active_reservation.id,
                        "name": active_reservation.user.name,
                        "vehicle_number": active_reservation.vehicle_number,
                        "parking_timestamp": active_reservation.parking_timestamp.isoformat()
                    }

            spots_data.append(spot_info)

        return {
            "lot": {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "price": lot.price,
                "maximum_number_of_spots": lot.maximum_number_of_spots,
                "available_spots_count": lot.available_spots_count,
                "occupied_spots_count": lot.occupied_spots_count
            },
            "spots": spots_data
        }, 200

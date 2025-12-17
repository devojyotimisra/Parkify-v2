from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot, ReserveParkingSpot
from application.helpers.decorators import admin_required
from datetime import datetime, timezone, timedelta


class AdminParkingSpotDetailsResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)

        if not spot:
            return {"error": "Parking spot not found"}, 404

        lot = ParkingLot.query.get(spot.lot_id)

        spot_data = {
            "id": spot.id,
            "lot_id": spot.lot_id,
            "status": spot.status,
            "lot": {
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "price": lot.price
            }
        }

        if spot.status == 'O':
            active_reservation = ReserveParkingSpot.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()
            now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
            parking_time = active_reservation.parking_timestamp.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
            hours_parked = (now - parking_time).total_seconds() / 3600
            estimated_cost = hours_parked * active_reservation.parking_cost_per_unit_time

            if active_reservation:
                spot_data["reservation"] = {
                    "id": active_reservation.id,
                    "name": active_reservation.user.name,
                    "email": active_reservation.user.email,
                    "address": active_reservation.user.address,
                    "pincode": active_reservation.user.pincode,
                    "vehicle_number": active_reservation.vehicle_number,
                    "parking_timestamp": active_reservation.parking_timestamp.isoformat(),
                    "hours_parked": hours_parked,
                    "estimated_cost": estimated_cost,
                    "parking_cost_per_unit_time": active_reservation.parking_cost_per_unit_time
                }

        return spot_data, 200

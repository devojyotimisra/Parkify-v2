from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.models import ParkingLot, ReserveParkingSpot, User
from application.helpers.decorators import user_required


class UserDashboardResource(Resource):
    @jwt_required()
    @user_required
    def get(self):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)

        vehicle_number = ""
        if user.vehicle_number:
            vehicle_number = user.vehicle_number

        active_reservations = ReserveParkingSpot.query.filter_by(user_id=current_user_id, leaving_timestamp=None).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
        parking_lots = ParkingLot.query.order_by(ParkingLot.prime_location_name.asc()).all()
        available_lots = [lot for lot in parking_lots if lot.available_spots_count > 0]

        active_res_data = []
        for res in active_reservations:
            lot = ParkingLot.query.get(res.lot_id) if res.lot_id else None
            active_res_data.append({
                "id": res.id,
                "lot_id": res.lot_id,
                "lot_name": lot.prime_location_name if lot else "N/A",
                "spot_id": res.spot_id,
                "vehicle_number": res.vehicle_number,
                "parking_timestamp": res.parking_timestamp.isoformat(),
                "parking_cost_per_unit_time": res.parking_cost_per_unit_time
            })

        available_lots_data = []
        for lot in available_lots:
            available_lots_data.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "available_spots_count": lot.available_spots_count,
                "maximum_number_of_spots": lot.maximum_number_of_spots
            })

        return {
            "vehicle_number": vehicle_number,
            "active_reservations": active_res_data,
            "available_lots": available_lots_data
        }, 200

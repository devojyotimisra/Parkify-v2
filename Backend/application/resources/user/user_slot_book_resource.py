from flask import current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone, timedelta
from application.helpers.models import ParkingLot, ParkingSpot, ReserveParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import user_required
from application.helpers.validators import validate_vehicle_number


class UserSlotBookResource(Resource):
    @jwt_required()
    @user_required
    def post(self, lot_id):
        current_user_id = int(get_jwt_identity())
        lot = ParkingLot.query.get(lot_id)

        if not lot:
            return {"error": "Parking lot not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('spot_id', type=int, required=True, help='Spot ID is required')
        parser.add_argument('vehicle_number', type=str, required=False)
        args = parser.parse_args()
        spot = ParkingSpot.query.get(args['spot_id'])

        if not spot or spot.lot_id != lot_id:
            return {"error": "Invalid spot for this parking lot"}, 400

        if spot.status != 'A':
            return {"error": "Spot is not available"}, 400

        if args['vehicle_number']:
            is_valid, result = validate_vehicle_number(args['vehicle_number'])
            if not is_valid:
                return {"error": result}, 400
            vehicle_number = result

        else:
            return {"error": "Vehicle number is required"}, 400

        if ReserveParkingSpot.query.filter(ReserveParkingSpot.vehicle_number == vehicle_number, ReserveParkingSpot.leaving_timestamp == None).first():
            return {"error": "This vehicle is already parked in another spot."}, 400

        spot.status = 'O'

        new_reservation = ReserveParkingSpot(
            lot_id=lot_id,
            spot_id=spot.id,
            user_id=current_user_id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now(timezone(timedelta(hours=5, minutes=30))),
            parking_cost_per_unit_time=lot.price
        )

        db.session.add(new_reservation)
        db.session.commit()

        current_app.bg_jobs.booking_confirmation_email_task.delay(new_reservation.id)

        return {"message": "Parking spot booked successfully"}, 201

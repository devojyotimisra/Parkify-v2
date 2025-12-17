from flask import current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone, timedelta
from application.helpers.models import ParkingSpot, ReserveParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import user_required


class UserSlotReleaseResource(Resource):
    @jwt_required()
    @user_required
    def post(self, reservation_id):
        current_user_id = int(get_jwt_identity())

        reservation = ReserveParkingSpot.query.get(reservation_id)

        if not reservation:
            return {"error": "Reservation not found"}, 404

        if reservation.user_id != current_user_id:
            return {"error": "Unauthorized access to this reservation"}, 403

        if reservation.leaving_timestamp:
            return {"error": "Reservation already completed"}, 400

        leaving_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        parking_time = reservation.parking_timestamp.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
        duration = (leaving_time - parking_time).total_seconds() / 3600
        total_cost = duration * reservation.parking_cost_per_unit_time

        reservation.leaving_timestamp = leaving_time
        reservation.duration_hours = round(duration, 2)
        reservation.total_cost = round(total_cost, 2)

        if reservation.spot_id:
            spot = ParkingSpot.query.get(reservation.spot_id)
            if spot:
                spot.status = 'A'

        db.session.commit()

        current_app.bg_jobs.slot_release_email_task.delay(reservation.id)

        return {"message": "Parking spot released successfully"}, 200
    
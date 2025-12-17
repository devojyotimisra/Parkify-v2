from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.helpers.models import ReserveParkingSpot, ParkingLot
from application.helpers.decorators import user_required


class UserHistoryResource(Resource):
    @jwt_required()
    @user_required
    def get(self):
        current_user_id = int(get_jwt_identity())
        reservations = ReserveParkingSpot.query.filter_by(user_id=current_user_id).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
        completed_reservations = [r for r in reservations if r.leaving_timestamp]
        completed_reservations.reverse()

        history_data = []
        for res in reservations:
            lot = ParkingLot.query.get(res.lot_id) if res.lot_id else None

            history_data.append({
                "id": res.id,
                "lot_name": f"{lot.prime_location_name} - {lot.address}" if lot else "Out of Service",
                "spot_id": res.spot_id,
                "vehicle_number": res.vehicle_number,
                "parking_timestamp": res.parking_timestamp.isoformat(),
                "leaving_timestamp": res.leaving_timestamp.isoformat() if res.leaving_timestamp else None,
                "parking_cost_per_unit_time": res.parking_cost_per_unit_time,
                "total_cost": float(res.total_cost) if res.total_cost else 0,
                "duration_hours": float(res.duration_hours) if res.duration_hours else 0,
                "status": "completed" if res.leaving_timestamp else "active"
            })

        active_reservations = [r for r in history_data if r['leaving_timestamp'] is None]
        active_reservations.sort(key=lambda x: x['parking_timestamp'], reverse=True)
        completed_reservations_list = [r for r in history_data if r['leaving_timestamp'] is not None]
        completed_reservations_list.sort(key=lambda x: x['leaving_timestamp'], reverse=True)
        history_data = active_reservations + completed_reservations_list

        chart_data = {
            'dates': [r.parking_timestamp.strftime('%Y-%m-%d') for r in completed_reservations],
            'costs': [float(r.total_cost) if r.total_cost else 0 for r in completed_reservations],
            'durations': [float(r.duration_hours) if r.duration_hours else 0 for r in completed_reservations]
        }

        return {"history": history_data, "chart_data": chart_data}, 200

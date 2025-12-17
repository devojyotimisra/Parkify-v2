from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.helpers.models import ReserveParkingSpot, ParkingLot
from application.helpers.decorators import admin_required


class AdminHistoryResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        reservations = ReserveParkingSpot.query.order_by(ReserveParkingSpot.leaving_timestamp.desc()).all()
        lots = ParkingLot.query.all()
        lot_revenue = {}
        lot_occupancy = {}

        for lot in lots:
            lot_occupancy[f"{lot.prime_location_name} - {lot.address}"] = {
                "total": lot.maximum_number_of_spots,
                "occupied": 0
            }

        history_data = []
        for res in reservations:
            if res.spot is None and ParkingLot.query.filter(ParkingLot.id == res.lot_id).first() != None:
                lot_name = f"{ParkingLot.query.filter(ParkingLot.id == res.lot_id).first().prime_location_name} - {ParkingLot.query.filter(ParkingLot.id == res.lot_id).first().address}"

            elif res.spot is None:
                lot_name = f'Out of Service'

            else:
                lot_name = f"{res.spot.lot.prime_location_name} - {res.spot.lot.address}"

            if res.leaving_timestamp is not None:
                lot_revenue[lot_name] = lot_revenue.get(lot_name, 0) + (res.total_cost or 0)

            history_data.append({
                "id": res.id,
                "lot_id": res.lot_id,
                "lot_name": lot_name,
                "spot_id": res.spot_id,
                "user_id": res.user_id,
                "vehicle_number": res.vehicle_number,
                "parking_timestamp": res.parking_timestamp.isoformat() if res.parking_timestamp else None,
                "leaving_timestamp": res.leaving_timestamp.isoformat() if res.leaving_timestamp else None,
                "parking_cost_per_unit_time": res.parking_cost_per_unit_time,
                "total_cost": res.total_cost,
                "duration_hours": res.duration_hours
            })

            if not lot_name=='Out of Service' and res.leaving_timestamp is None:
                lot_occupancy[lot_name]["occupied"] += 1

        lot_revenue = dict(sorted(lot_revenue.items()))
        lot_occupancy = dict(sorted(lot_occupancy.items()))
        active_reservations = [r for r in history_data if r['leaving_timestamp'] is None]
        active_reservations.sort(key=lambda x: x['parking_timestamp'], reverse=True)
        completed_reservations = [r for r in history_data if r['leaving_timestamp'] is not None]
        completed_reservations.sort(key=lambda x: x['leaving_timestamp'], reverse=True)
        history_data = active_reservations + completed_reservations

        chart_data = {
            "revenue": {
                "labels": list(lot_revenue.keys()),
                "data": list(lot_revenue.values())
            },
            "occupancy": {
                "labels": list(lot_occupancy.keys()),
                "available": [lot_occupancy[lot]["total"] - lot_occupancy[lot]["occupied"] for lot in lot_occupancy],
                "occupied": [lot_occupancy[lot]["occupied"] for lot in lot_occupancy]
            }
        }

        total_revenue = sum(lot_revenue.values())

        return {
            "history": history_data,
            "chart_data": chart_data,
            "analytics": {
                "total_revenue": float(total_revenue),
                "total_completed_reservations": len(completed_reservations),
                "active_reservations": len(active_reservations)
            }
        }, 200

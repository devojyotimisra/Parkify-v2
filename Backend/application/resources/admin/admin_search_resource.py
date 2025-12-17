from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, User, ReserveParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import admin_required


class AdminSearchResource(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('search_type', type=str, required=True, help='Search type is required')
        parser.add_argument('query', type=str, required=True, help='Query is required')
        args = parser.parse_args()
        search_type = args['search_type']
        query = args['query']

        if search_type == 'lot':
            if query:
                lots = ParkingLot.query.filter(
                    (ParkingLot.prime_location_name.ilike(f'%{query}%')) |
                    (ParkingLot.address.ilike(f'%{query}%')) |
                    (ParkingLot.pin_code.ilike(f'%{query}%'))
                ).all()

            else:
                lots = ParkingLot.query.all()

            results = []
            for lot in lots:
                results.append({
                    "id": lot.id,
                    "prime_location_name": lot.prime_location_name,
                    "price": lot.price,
                    "address": lot.address,
                    "pin_code": lot.pin_code,
                    "maximum_number_of_spots": lot.maximum_number_of_spots,
                    "available_spots_count": lot.available_spots_count,
                    "occupied_spots_count": lot.occupied_spots_count
                })

            return {"type": "lot", "results": results}, 200

        elif search_type == 'user':
            if query:
                users = User.query.filter(
                    (User.name.ilike(f'%{query}%')) |
                    (User.email.ilike(f'%{query}%')) |
                    (User.address.ilike(f'%{query}%'))
                ).all()

            else:
                users = User.query.all()

            results = []
            for user in users:
                user_roles = [role.name for role in user.roles]
                
                if 'user' in user_roles:
                    results.append({
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "address": user.address,
                        "pincode": user.pincode,
                        "vehicle_number": user.vehicle_number,
                        "active": user.active
                    })

            return {"type": "user", "results": results}, 200

        elif search_type == 'vehicle':
            results = []
            vehicle_numbers = set()

            if query:
                res_vehicles = db.session.query(ReserveParkingSpot.vehicle_number).filter(ReserveParkingSpot.vehicle_number.ilike(f'%{query}%')).distinct().all()
                for v in res_vehicles:
                    vehicle_numbers.add(v[0])

                user_vehicles = db.session.query(User.vehicle_number).filter(User.vehicle_number.ilike(f'%{query}%')).distinct().all()
                for v in user_vehicles:
                    if v[0]:
                        vehicle_numbers.add(v[0])

            else:
                res_vehicles = db.session.query(ReserveParkingSpot.vehicle_number).distinct().all()
                for v in res_vehicles:
                    vehicle_numbers.add(v[0])

                user_vehicles = db.session.query(User.vehicle_number).distinct().all()
                for v in user_vehicles:
                    if v[0]:
                        vehicle_numbers.add(v[0])

            for vehicle_number in vehicle_numbers:
                last_reservation = ReserveParkingSpot.query.filter_by(vehicle_number=vehicle_number).order_by(ReserveParkingSpot.parking_timestamp.desc()).first()

                if last_reservation:
                    user = User.query.get(last_reservation.user_id) if last_reservation.user_id else None

                    if user:
                        results.append({
                            "vehicle_number": vehicle_number,
                            "user_id": user.id,
                            "user_email": user.email,
                            "user_name": user.name,
                            "user_active": user.active
                        })

                    else:
                        results.append({
                            "vehicle_number": vehicle_number,
                            "user_id": "Deleted User",
                            "user_email": "Deleted User",
                            "user_name": "Deleted User",
                            "user_active": False
                        })

                else:
                    user = User.query.filter_by(vehicle_number=vehicle_number).first()

                    if user:
                        results.append({
                            "vehicle_number": vehicle_number,
                            "user_id": user.id,
                            "user_email": user.email,
                            "user_name": user.name,
                            "user_active": user.active
                        })

                    else:
                        results.append({
                            "vehicle_number": vehicle_number,
                            "user_id": "N/A",
                            "user_email": "N/A",
                            "user_name": "Unknown",
                            "user_active": False
                        })

            return {"type": "vehicle", "results": results}, 200

        else:
            return {"error": "Invalid search type. Use 'lot', 'user', or 'vehicle'"}, 400

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot
from application.helpers.decorators import user_required


class UserSearchResource(Resource):
    @jwt_required()
    @user_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, required=True, help='Location is required')
        args = parser.parse_args()

        location = args['location']
        lots = ParkingLot.query.filter(
            (ParkingLot.prime_location_name.ilike(f'%{location}%')) |
            (ParkingLot.address.ilike(f'%{location}%')) |
            (ParkingLot.pin_code.ilike(f'%{location}%'))
        ).all()

        available_lots = [lot for lot in lots if lot.available_spots_count > 0]

        results = []
        for lot in available_lots:
            results.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "price": lot.price,
                "address": lot.address,
                "pin_code": lot.pin_code,
                "available_spots_count": lot.available_spots_count,
                "maximum_number_of_spots": lot.maximum_number_of_spots
            })

        return {"results": results}, 200

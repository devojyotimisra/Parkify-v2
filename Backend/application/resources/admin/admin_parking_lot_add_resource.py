from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import admin_required
from application.helpers.validators import validate_name, validate_address, validate_pincode, validate_price, validate_spot_count


class AdminParkingLotAddResource(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prime_location_name', type=str, required=True, help='Location name is required')
        parser.add_argument('price', required=True, help='Price is required')
        parser.add_argument('address', type=str, required=True, help='Address is required')
        parser.add_argument('pin_code', required=True, help='Pin code is required')
        parser.add_argument('maximum_number_of_spots', required=True, help='Number of spots is required')
        args = parser.parse_args()

        is_valid, result = validate_name(args['prime_location_name'])
        if not is_valid:
            return {"error": result}, 400
        location_name = result

        is_valid, result = validate_price(args['price'])
        if not is_valid:
            return {"error": result}, 400
        price = result

        is_valid, result = validate_address(args['address'])
        if not is_valid:
            return {"error": result}, 400
        address = result

        is_valid, result = validate_pincode(args['pin_code'])
        if not is_valid:
            return {"error": result}, 400
        pin_code = result

        is_valid, result = validate_spot_count(args['maximum_number_of_spots'])
        if not is_valid:
            return {"error": result}, 400
        max_spots = result

        new_lot = ParkingLot(
            prime_location_name=location_name,
            price=price,
            address=address,
            pin_code=pin_code,
            maximum_number_of_spots=max_spots
        )

        db.session.add(new_lot)
        db.session.commit()

        for _ in range(max_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status='A')
            db.session.add(spot)

        db.session.commit()

        return {
            "message": "Parking lot created successfully",
            "lot": {
                "id": new_lot.id,
                "prime_location_name": new_lot.prime_location_name,
                "price": new_lot.price,
                "address": new_lot.address,
                "pin_code": new_lot.pin_code,
                "maximum_number_of_spots": new_lot.maximum_number_of_spots
            }
        }, 201

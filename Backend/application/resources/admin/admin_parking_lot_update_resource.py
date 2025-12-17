from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from application.helpers.models import ParkingLot, ParkingSpot
from application.extensions.db_extn import db
from application.helpers.decorators import admin_required
from application.helpers.validators import validate_name, validate_address, validate_pincode, validate_price


class AdminParkingLotUpdateResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)

        if not lot:
            return {"error": "Parking lot not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('prime_location_name', type=str)
        parser.add_argument('price')
        parser.add_argument('address', type=str)
        parser.add_argument('pin_code')
        parser.add_argument('maximum_number_of_spots', type=int)
        args = parser.parse_args()

        if args['prime_location_name']:
            is_valid, result = validate_name(args['prime_location_name'])
            if not is_valid:
                return {"error": result}, 400
            lot.prime_location_name = result

        if args['price']:
            is_valid, result = validate_price(args['price'])
            if not is_valid:
                return {"error": result}, 400
            lot.price = result

        if args['address']:
            is_valid, result = validate_address(args['address'])
            if not is_valid:
                return {"error": result}, 400
            lot.address = result

        if args['pin_code']:
            is_valid, result = validate_pincode(args['pin_code'])
            if not is_valid:
                return {"error": result}, 400
            lot.pin_code = result

        if args['maximum_number_of_spots'] is not None:
            new_spots = args['maximum_number_of_spots']
            current_spots = lot.maximum_number_of_spots

            if new_spots > current_spots:
                for _ in range(new_spots - current_spots):
                    db.session.add(ParkingSpot(lot_id=lot.id))
                    
            elif new_spots < current_spots:
                reserved = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
                if new_spots < reserved:
                    return {"error": f"Cannot reduce spots below {reserved} (currently reserved)"}, 400
                deletable = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').all()
                for spot in deletable[:current_spots - new_spots]:
                    db.session.delete(spot)

            lot.maximum_number_of_spots = new_spots

        db.session.commit()

        return {"message": "Parking lot updated successfully"}, 200

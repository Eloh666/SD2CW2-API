from datetime import datetime
from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.bookings import Booking
from models.databaseInit import db


class BookingController(Resource):
    # decorators = [jwt_required()]

    def get(self):
        bookings = Booking.query.all()
        query = []
        for i in bookings:
            myDict = {
                'id': i.id,
                'arrivalDate': str(i.arrivalDate),
                'departureDate': str(i.departureDate),
                'customerId': i.customerId
            }
            query.append(myDict)
        return query

    def post(self):
        body = request.get_json()
        arrival = datetime.strptime(body.get('arrival'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departure'), '%Y-%m-%d')
        customerId = body.get('customerId')
        if customerId:
            db.session.add(Booking(arrival, departure, customerId))
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def put(self):
        return {"response": "put the booking"}

    def delete(self):
        return {"response": "delete the booking"}

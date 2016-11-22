from datetime import datetime
from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.bookings import Booking
from models.customers import Customer
from models.databaseInit import db


class BookingController(Resource):
    # decorators = [jwt_required()]

    def get(self):
        bookings = Booking.query.all()
        query = []
        for i in bookings:
            myDict = {
                'ArrivalDate': str(i.arrivalDate),
                'DepartureDate': str(i.departureDate),
                'CustomerId': i.customerId,
                'DietaryReqs': i.dietaryReqs,
                'Guests': i.guests,
                'Extras': i.extras
            }
            query.append(myDict)
        return query

    def post(self):
        body = request.get_json()
        guests = body.get('guests')
        extras = body.get('extras')
        arrival = datetime.strptime(body.get('arrivalDate'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departureDate'), '%Y-%m-%d')
        customerId = body.get('customerId')
        if customerId and Customer.query.filter_by(referenceNumber=customerId).first():
            db.session.add(Booking(arrival, departure, customerId, guests, extras))
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def put(self):
        body = request.get_json()
        id = body.get('id')
        arrival = datetime.strptime(body.get('arrivalDate'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departureDate'), '%Y-%m-%d')
        customerId = body.get('customerId')
        booking = Booking.query.filter_by(id=id).first()
        if booking and Customer.query.filter_by(referenceNumber=customerId).first():
            booking.arrivalDate = arrival
            booking.departureDate = departure
            booking.customerId = customerId
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def delete(self):
        body = request.get_json()
        id = body.get("id")
        deleted = Booking.query.filter_by(id=id).delete()
        db.session.commit()
        return {"response": {"ok": True, "deleted": True if deleted == 1 else False}}


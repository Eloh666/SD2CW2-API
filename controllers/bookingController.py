from datetime import datetime
from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.bookings import Booking
from models.customers import Customer
from models.guest import addAllGuestsByBookingId, deleteAllGuestsByBookingId
from models.extras import addAllExtrasByBookingId, deleteAllExtrasByBookingId
from models.databaseInit import db



def alc2json(row):
    return dict([(col, str(getattr(row,col))) for col in row.__table__.columns.keys()])

class BookingController(Resource):
    # decorators = [jwt_required()]

    def get(self):
        bookings = Booking.query.all()
        query = []
        for i in bookings:
            guests = [alc2json(guest) for guest in i.guests]
            extras = {}
            for k in [alc2json(extra) for extra in i.extras]:
                extras[k['type']] = k if k['type'] == 'carHire' else True
            myDict = {
                'Id': str(i.id),
                'ArrivalDate': str(i.arrivalDate),
                'DepartureDate': str(i.departureDate),
                'CustomerId': i.customerId,
                'DietaryReqs': i.dietaryReqs,
                'Guests': guests,
                'Extras': extras
            }
            query.append(myDict)
        return query

    def post(self):
        body = request.get_json()
        extras = dict(body.get('extras'))
        arrival = datetime.strptime(body.get('arrivalDate'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departureDate'), '%Y-%m-%d')
        customerId = body.get('customerId')
        if customerId and Customer.query.filter_by(referenceNumber=customerId).first():
            newBooking = Booking(arrival, departure, customerId)
            db.session.add(newBooking)
            db.session.commit()
            db.session.bulk_save_objects(addAllGuestsByBookingId(body.get('guests'), newBooking.id))
            db.session.bulk_save_objects(addAllExtrasByBookingId(extras, newBooking.id))
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Customer not found"}}

    def put(self):
        body = request.get_json()
        bookingId = body.get('id')
        arrival = datetime.strptime(body.get('arrivalDate'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departureDate'), '%Y-%m-%d')
        dietaryReqs = body.get('dietaryReqs')
        customerId = body.get('customerId')
        booking = Booking.query.filter_by(id=bookingId).first()
        if booking and Customer.query.filter_by(referenceNumber=customerId).first():
            booking.arrivalDate = arrival
            booking.departureDate = departure
            booking.customerId = customerId
            booking.dietaryReqs = dietaryReqs
            db.session.commit()
            deleteAllGuestsByBookingId(bookingId)
            deleteAllExtrasByBookingId(bookingId)
            db.session.bulk_save_objects(addAllGuestsByBookingId(body.get('guests'), booking.id))
            db.session.bulk_save_objects(addAllExtrasByBookingId(body.get('extras'), booking.id))
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def delete(self):
        body = request.get_json()
        bookingId = body.get("id")
        deleted = Booking.query.filter_by(id=bookingId).delete()
        deleteAllGuestsByBookingId(bookingId)
        deleteAllExtrasByBookingId(bookingId)
        db.session.commit()
        return {"response": {"ok": True, "deleted": True if deleted == 1 else False}}


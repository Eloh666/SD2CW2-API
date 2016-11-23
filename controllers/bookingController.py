from datetime import datetime
from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request, jsonify

from models.bookings import Booking
from models.customers import Customer
from models.guest import Guest
from models.extras import Extra
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
        guestsList = []
        extrasList = []
        extras = dict(body.get('extras'))
        arrival = datetime.strptime(body.get('arrivalDate'), '%Y-%m-%d')
        departure = datetime.strptime(body.get('departureDate'), '%Y-%m-%d')
        customerId = body.get('customerId')
        if customerId and Customer.query.filter_by(referenceNumber=customerId).first():
            newBooking = Booking(arrival, departure, customerId)
            db.session.add(newBooking)
            print(newBooking.id)
            db.session.commit()
            for guest in body.get('guests'):
                guestsList.append(Guest(
                    guest['name'], guest['age'],
                    guest['passport'],
                    newBooking.id))
            for key, value in extras.items():
                print(key)
                print(value)
                if value:
                    if key == 'carHire':
                        extrasList.append(Extra(
                            key,
                            newBooking.id,
                            datetime.strptime(value['hireStart'], '%Y-%m-%d'),
                            datetime.strptime(value['hireEnd'], '%Y-%m-%d')))
                    else:
                        extrasList.append(Extra(key, newBooking.id))
            db.session.bulk_save_objects(guestsList)
            db.session.bulk_save_objects(extrasList)
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Customer not found"}}

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


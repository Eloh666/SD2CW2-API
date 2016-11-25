from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.bookings import Booking
from models.customers import Customer
from models.databaseInit import db


class CustomerController(Resource):
    # decorators = [jwt_required()]

    def get(self):
        customers = Customer.query.all()
        query = []
        for i in customers:
            myDict = {
                'ReferenceNumber': i.referenceNumber,
                'Name': i.name,
                'Address': i.address
            }
            query.append(myDict)
        return query

    def post(self):
        body = request.get_json()
        referenceNumber = body.get("referenceNumber")
        name = body.get("name")
        address = body.get("address")
        if referenceNumber and name and address:
            db.session.add(Customer(referenceNumber, name, address))
            db.session.commit()
            return {"response": {"ok": True, "id": referenceNumber}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def put(self):
        body = request.get_json()
        referenceNumber = body.get("referenceNumber")
        name = body.get("name")
        address = body.get("address")
        customer = Customer.query.filter_by(referenceNumber=referenceNumber).first()
        if customer:
            customer.name = name
            customer.address = address
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def delete(self):
        body = request.get_json()
        referenceNumber = body.get("referenceNumber")
        if not Booking.query.filter_by(customerId=referenceNumber).first():
            Customer.query.filter_by(referenceNumber=referenceNumber).delete()
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

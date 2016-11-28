from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.bookings import Booking
from models.customers import Customer, serializeCustomer
from models.databaseInit import db


class CustomerController(Resource):
    decorators = [jwt_required()]

    def get(self):
        customers = Customer.query.all()
        query = []
        for customer in customers:
            query.append(serializeCustomer(customer))
        return query

    def post(self):
        body = request.get_json()
        name = body.get("name")
        address = body.get("address")
        if name and address:
            newCustomer = Customer(name, address)
            db.session.add(newCustomer)
            db.session.commit()
            return serializeCustomer(newCustomer)
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}, 500

    def put(self):
        body = request.get_json()
        referenceNumber = body.get("referencenumber")
        name = body.get("name")
        address = body.get("address")
        customer = Customer.query.filter_by(referenceNumber=referenceNumber).first()
        if customer:
            customer.name = name
            customer.address = address
            db.session.commit()
            return serializeCustomer(customer)
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}, 500

    def delete(self):
        body = request.get_json()
        referenceNumber = body.get("referencenumber")
        if not Booking.query.filter_by(customerId=referenceNumber).first():
            Customer.query.filter_by(referenceNumber=referenceNumber).delete()
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

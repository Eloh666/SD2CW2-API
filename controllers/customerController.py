from flask_jwt import jwt_required
from flask_restful import Resource
from flask import request

from models.customers import Customer
from models.databaseInit import db


class CustomerController(Resource):
    # decorators = [jwt_required()]

    def get(self):
        customers = Customer.query.all()
        return {"response": "Getting the booking"}

    def post(self):
        body = request.get_json()
        print(body)
        referenceNumber = body.get("referenceNumber")
        name = body.get("name")
        address = body.get("address")
        if referenceNumber and name and address:
            db.session.add(Customer(referenceNumber, name, address))
            db.session.commit()
            return {"response": {"ok": True}}
        return {"response": {"ok": False, "Error": "Something went wrong with sending the data"}}

    def put(self):
        return {"response": "put the booking"}

    def delete(self):
        return {"response": "delete the booking"}

from authentication.authenticateUser import checkUser
from flask_jwt import jwt_required
from flask_restful import Resource


class BookingController(Resource):
    decorators = [checkUser, jwt_required()]

    def get(self):
        return {"response": "Getting the booking"}

    def post(self):
        return {"response": "post the booking"}

    def put(self):
        return {"response": "put the booking"}

    def delete(self):
        return {"response": "delete the booking"}

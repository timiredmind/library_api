from flask_restful import Resource
from flask import request
from schemas.user import UserSchema
from marshmallow import ValidationError
from http import HTTPStatus
from models.user import User
from extension import db
from flask_jwt_extended import create_access_token
from utils import verify_password

class CreateUserResource(Resource):
    def post(self):
        # Retrieve JSON data from the request
        json_data = request.get_json()
        # Deserialize and validate the JSON data
        try:
            parsed_data = UserSchema().load(json_data)
        except ValidationError as errors:
            return {"message": "Validation Error", "errors": errors.messages}, HTTPStatus.BAD_REQUEST
        # Check if username already exist
        username = parsed_data.get("username")
        email = parsed_data.get("email")

        if User.check_username(username):
            return {"message": "Invalid username or username is associated to a different user."}, HTTPStatus.CONFLICT

        if User.check_email(email):
            return {
                       "message": "Invalid email address or email address is associated to a different user."
                   }, HTTPStatus.CONFLICT

        new_user = User(**parsed_data)
        db.session.add(new_user)
        db.session.commit()
        return UserSchema(exclude=("password", "date_last_updated")).dump(new_user), HTTPStatus.CREATED


class UserLoginResource(Resource):
    def post(self):
        json_data = request.get_json()
        try:
            UserSchema(only=("username", "password")).load(json_data)
        except ValidationError as errors:
            return {
                "message": "Validation Error",
                "errors": [errors.messages]
            }, HTTPStatus.BAD_REQUEST

        username = json_data.get("username")
        plain_text = json_data.get("password")

        user = User.check_username(username)
        if (user is None) or verify_password(plain_text, user.password) is False or user.is_active is False:
            return "Invalid username or password.", HTTPStatus.UNAUTHORIZED

        claims = {"role": user.role}
        access_token = create_access_token(identity=user.id, additional_claims=claims)
        return {"access_token": access_token}, HTTPStatus.OK

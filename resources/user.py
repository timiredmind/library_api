from flask_restful import Resource
from flask import request
from schemas.user import UserSchema
from marshmallow import ValidationError
from http import HTTPStatus
from models.user import User
from extension import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        if (not user) or (not verify_password(plain_text, user.password))  or (not user.is_active):
            return "Invalid username or password.", HTTPStatus.UNAUTHORIZED

        claims = {"role": user.role}
        access_token = create_access_token(identity=user.id, additional_claims=claims)
        return {"access_token": access_token}, HTTPStatus.OK


class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.check_user_id(user_id=user_id)
        return UserSchema(exclude=("password", "date_last_updated")).dump(user), HTTPStatus.OK

    @jwt_required()
    def patch(self):
        json_data = request.get_json()
        try:
            UserSchema(partial=True, exclude=["password"]).load(json_data)
        except ValidationError as errors:
            return {
                "message": "Validation Error",
                "errors": [errors.messages]
            }, HTTPStatus.BAD_REQUEST

        user_id = get_jwt_identity()
        user = User.check_user_id(user_id=user_id)

        username = json_data.get("username")
        email = json_data.get("email")

        if username != user.username and User.check_username(username):
            return {"message": "Username already associated with a different user."}, HTTPStatus.CONFLICT

        if email != user.email and user.check_email(email):
            return {"message": "Email address associated with a different user."}, HTTPStatus.CONFLICT
        user.username = username or user.username
        user.email = email or user.email
        db.session.commit()
        return UserSchema().dump(user), HTTPStatus.OK

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.check_user_id(user_id)
        user.is_active = False
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT

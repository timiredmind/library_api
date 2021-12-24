from marshmallow import fields, Schema
from passlib.hash import bcrypt


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize="hash_password")
    is_active = fields.Boolean(dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    date_last_updated = fields.DateTime(dump_only=True)

    def hash_password(self, plain_text):
        hashed_password = bcrypt.using(rounds=6).hash(plain_text)
        return hashed_password




from marshmallow import fields, Schema
from schemas.user import UserSchema
# from schemas.book import BookSchema


class BooksBorrowedSchema(Schema):
    id = fields.Int(dump_only=True)
    user = fields.Nested(UserSchema(only=["username"]), attribute="user", dump_only=True)
    date_borrowed = fields.DateTime(dump_only=True)
    date_returned = fields.DateTime(dump_only=True)


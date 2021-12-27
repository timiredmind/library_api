from marshmallow import fields, Schema
from schemas.author import AuthorSchema
from schemas.publisher import PublisherSchema
from schemas.category import CategorySchema
from schemas.borrowed_book import BooksBorrowedSchema


class BookSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    num_of_pages = fields.Int(required=True)
    isbn = fields.Str(required=True)
    isbn13 = fields.Str(required=True)
    language = fields.Str(required=True)
    year_published = fields.Int(required=True)
    cover_url = fields.URL()
    is_available = fields.Bool(dump_only=True)
    author_ = fields.Nested(AuthorSchema(exclude=["id"]), attribute="author", dump_only=True)
    publisher_ = fields.Nested(PublisherSchema(exclude=["id"]), attribute="publisher", dump_only=True)
    category_ = fields.Nested(CategorySchema(exclude=["id"]), attribute="category", dump_only=True)
    date_donated = fields.DateTime(dump_only=True)
    author = fields.Str(load_only=True)
    publisher = fields.Str(load_only=True)
    category = fields.Str(load_only=True)
    loan_history = fields.Nested(BooksBorrowedSchema(many=True), attribute="book_loan_history")


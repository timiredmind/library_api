from marshmallow import fields, Schema
from passlib.hash import bcrypt
from .pagination import PaginationSchema


class UserSchema(Schema):
    class Meta:
        ordered=True
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


class BookLoanHistorySchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    boorowed_by = fields.Nested(UserSchema(only=["username"]), attribute="user", dump_only=True)
    date_borrowed = fields.DateTime(dump_only=True)
    date_returned = fields.DateTime(dump_only=True)


class AuthorCollectionSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()


class CategoryCollectionSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PublisherCollectionSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


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
    author_ = fields.Nested(AuthorCollectionSchema(only=["name"]), attribute="author", dump_only=True)
    publisher_ = fields.Nested(PublisherCollectionSchema(exclude=["id"]), attribute="publisher", dump_only=True)
    category_ = fields.Nested(CategoryCollectionSchema(exclude=["id"]), attribute="category", dump_only=True)
    date_donated = fields.DateTime(dump_only=True)
    author = fields.Str(load_only=True)
    publisher = fields.Str(load_only=True)
    category = fields.Str(load_only=True)
    loan_history = fields.Nested(BookLoanHistorySchema(many=True, exclude=["id"]), attribute="book_loan_history")


class BooksBorrowedSchema(Schema):
    class Meta:
        ordered = True
    id = fields.Int(dump_only=True)
    book = fields.Nested(BookSchema(only=["name"]), attribute="book", dump_only=True)
    date_borrowed = fields.DateTime(dump_only=True)
    date_returned = fields.DateTime(dump_only=True)


class AuthorSchema(AuthorCollectionSchema):
    books = fields.Nested(BookSchema(only=["id", "name", "cover_url"]), many=True, attribute="books")


class CategorySchema(CategoryCollectionSchema):
    books = fields.Nested(BookSchema(only=["id", "name", "cover_url"]), many=True, attribute="books")


class PublisherSchema(PublisherCollectionSchema):
    books = fields.Nested(BookSchema(only=["id", "name", "cover_url"]), many=True, attribute="books")


class UserSchema2(UserSchema):
    books_borrowed = fields.Nested(BooksBorrowedSchema(many=True, exclude=["id"]), attribute="books_borrowed")


class PaginatedBookSchema(PaginationSchema):
    books = fields.Nested(BookSchema(only=["id", "name", "author_", "cover_url"], many=True), attribute="items")


class PaginatedAuthorSchema(PaginationSchema):
    authors = fields.Nested(AuthorCollectionSchema(many=True, only=["id", "name"]), attribute="items")


class PaginatedCategorySchema(PaginationSchema):
    categories = fields.Nested(CategoryCollectionSchema(many=True), attribute="items")


class PaginatedPublisherSchema(PaginationSchema):
    publishers = fields.Nested(PublisherCollectionSchema(many=True), attribute="items")
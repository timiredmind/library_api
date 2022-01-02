from utils import admin_required
from flask_restful import Resource
from models.user import User
from models.book import Book, Category, Publisher, Author
from schemas.book import PaginatedUserSchema, UserSchema2, PaginatedBookSchema
from webargs.flaskparser import use_kwargs
from webargs import fields
from sqlalchemy import asc, desc, and_
from http import HTTPStatus
from extension import db
from datetime import datetime
from flask import request
from marshmallow import ValidationError
from schemas.book import BookSchema


class AdminUsersCollectionResource(Resource):
    @admin_required()
    @use_kwargs({
        "page": fields.Integer(missing=1),
        "per_page": fields.Integer(missing=5),
        "sort": fields.String(missing="id"),
        "order": fields.String(missing="asc")
    }, location="querystring")
    def get(self, page, per_page, sort, order):
        if sort not in ["id", "username"]:
            sort = "id"
        if order == "desc":
            sort_logic = desc(getattr(User, sort))
        else:
            sort_logic = asc(getattr(User, sort))

        users = User.query.order_by(sort_logic).paginate(page=page, per_page=per_page)
        return PaginatedUserSchema().dump(users), HTTPStatus.OK


class AdminUsersResource(Resource):
    @admin_required()
    def get(self, user_id):
        user = User.check_user_id(user_id=user_id)
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        return UserSchema2(exclude=["id"]).dump(user), HTTPStatus.OK

    @admin_required()
    def delete(self, user_id):
        user = User.check_user_id(user_id=user_id)
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND
        if not user.is_active:
            return {"message": "User already deactivated."}, HTTPStatus.CONFLICT
        user.is_active = False
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class AdminBooksCollectionResource(Resource):
    @admin_required()
    @use_kwargs({
        "page": fields.Integer(missing=1),
        "per_page": fields.Integer(missing=5),
        "order": fields.Str(missing="asc"),
        "sort": fields.Str(missing="id"),
        "q": fields.Str(missing=""),
        "max_publication_year": fields.Int(missing=datetime.now().year),
        "min_publication_year": fields.Int(missing=1980),
        "max_page_num": fields.Int(missing=5000),
        "min_page_num": fields.Int(missing=0)
    }, location="querystring")
    def get(self,
            page, per_page, order, sort, q, max_publication_year, min_publication_year, min_page_num, max_page_num):
        keyword = f"%{q}%"
        if sort not in ["id", "num_of_pages", "date_donated", "year_published", "name"]:
            sort = "id"
        if order == 'desc':
            sort_logic = desc(getattr(Book, sort))
        else:
            sort_logic = asc(getattr(Book, sort))
        books = Book.query.filter(
            Book.name.ilike(keyword),
            and_(Book.year_published <= max_publication_year, Book.year_published >= min_publication_year),
            and_(Book.num_of_pages <= max_page_num, Book.num_of_pages >= min_page_num)
        ).order_by(sort_logic).paginate(page=page, per_page=per_page)
        return PaginatedBookSchema().dump(books), HTTPStatus.OK

    @admin_required()
    def post(self):
        json_data = request.get_json()
        print(json_data)
        try:
            parsed_data = BookSchema().load(json_data)
        except ValidationError as errors:
            return {"message": "Validation Error",
                    "errors": [errors.messages]
                   }, HTTPStatus.BAD_REQUEST

        name = parsed_data.get("name")
        num_of_pages = parsed_data.get("num_of_pages")
        isbn = parsed_data.get("isbn")
        isbn13 = parsed_data.get("isbn13")
        language = parsed_data.get("language")
        year_published = parsed_data.get("year_published")
        cover_url = parsed_data.get("cover_url")
        author_name = parsed_data.get("author")
        category_name = parsed_data.get("category")
        publisher_name = parsed_data.get("publisher")

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)

        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)

        publisher = Publisher.query.filter_by(name=publisher_name).first()
        if not publisher:
            publisher = Publisher(name=publisher_name)

        new_book = Book(
            name=name, num_of_pages=num_of_pages, isbn=isbn, isbn13=isbn13, year_published=year_published,
            cover_url=cover_url, language=language)
        new_book.author = author
        new_book.category = category
        new_book.publisher = publisher
        db.session.add(new_book)
        db.session.commit()
        return BookSchema(exclude=["loan_history"]).dump(new_book), HTTPStatus.CREATED


class AdminBookResource(Resource):
    @admin_required()
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {'message': "Book not found"}, HTTPStatus.NOT_FOUND

        return BookSchema().dump(book), HTTPStatus.OK

    @admin_required()
    def patch(self, book_id):
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return {"message": "Book not found"}, HTTPStatus.NOT_FOUND

        json_data = request.get_json()
        try:
            parsed_data = BookSchema(exclude=["author", "publisher", "category"], partial=True).load(json_data)

        except ValidationError as err:
            return {
                "messages": "Validation Error",
                "errors": [err.messages]
            }, HTTPStatus.BAD_REQUEST

        book.name = parsed_data.get("name") or book.name
        book.year_published = parsed_data.get("year_published") or book.year_published
        book.num_of_pages = parsed_data.get("num_of_pages") or book.num_of_pages
        book.language = parsed_data.get("language") or book.language
        book.cover_url = parsed_data.get("cover_url") or book.cover_url
        book.isbn13 = parsed_data.get("isbn13") or book.isbn13
        book.isbn = parsed_data.get("isbn") or book.isbn

        db.session.commit()
        return BookSchema().dump(book), HTTPStatus.OK


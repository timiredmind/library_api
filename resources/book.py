from datetime import datetime
from http import HTTPStatus
from extension import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import asc, desc, and_
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.user import User
from models.book import Book, BooksBorrowed
from schemas.book import PaginatedBookSchema, BookSchema


class BookCollectionResource(Resource):
    @jwt_required()
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


class BookResource(Resource):
    @jwt_required()
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {"message": "Book not found!"}, HTTPStatus.NOT_FOUND

        return BookSchema(exclude=["id", "loan_history", "date_donated", "is_available"]).dump(book), HTTPStatus.OK


class BorrowBookResource(Resource):
    @jwt_required()
    def patch(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {"message": "Book not found."}, HTTPStatus.NOT_FOUND

        if book.is_available is False:
            return {"message": "Book is currently unavailable"}, HTTPStatus.NOT_FOUND

        book.is_available = False
        user_id = get_jwt_identity()
        user = User.check_user_id(user_id)
        loan_detail = BooksBorrowed()
        loan_detail.book = book
        loan_detail.user = user
        db.session.add(loan_detail)
        db.session.commit()
        return "", HTTPStatus.NO_CONTENT


class ReturnBookResource(Resource):
    @jwt_required()
    def patch(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {"message": "Book not found."}, HTTPStatus.NOT_FOUND
        user_id = get_jwt_identity()
        loan_detail = BooksBorrowed.query.filter(
            and_(BooksBorrowed.user_id == user_id, BooksBorrowed.book_id == book_id)).filter_by(
            date_returned=None).first()

        if not loan_detail:
            return {"message": "Unauthorized Access"}, HTTPStatus.CONFLICT

        book.is_available = True
        loan_detail.date_returned = datetime.now()
        db.session.commit()
        return {"message": "Book returned !"}, HTTPStatus.OK



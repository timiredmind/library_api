from flask_restful import Resource
from models.book import Book
from flask_jwt_extended import jwt_required
from schemas.book import PaginatedBookSchema, BookSchema
from http import HTTPStatus
from webargs.flaskparser import use_kwargs
from webargs import fields
from sqlalchemy import asc, desc, or_, and_
from datetime import datetime


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

        return BookSchema(exclude=["id"]).dump(book), HTTPStatus.OK

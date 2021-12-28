from flask_restful import Resource
from models.book import Book
from flask_jwt_extended import jwt_required
from schemas.book import BookSchema
from http import HTTPStatus


class BookCollectionResource(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        return BookSchema(only=["id", "author_", "cover_url"], many=True).dump(books), HTTPStatus.OK


class BookResource(Resource):
    @jwt_required()
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return {"message": "Book not found!"}, HTTPStatus.NOT_FOUND

        return BookSchema().dump(book), HTTPStatus.OK

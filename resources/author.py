from models.book import Author
from flask_restful import Resource
from schemas.book import AuthorCollectionSchema, AuthorSchema
from http import HTTPStatus
from flask_jwt_extended import jwt_required


class AuthorCollectionResource(Resource):
    @jwt_required()
    def get(self):
        authors = Author.query.all()
        return AuthorCollectionSchema(many=True, only=["id", "name"]).dump(authors), HTTPStatus.OK


class AuthorResource(Resource):
    @jwt_required()
    def get(self, author_id):
        author = Author.query.filter_by(id=author_id).first()
        if not author:
            return {"message": "Author not found!"}, HTTPStatus.NOT_FOUND
        return AuthorSchema().dump(author), HTTPStatus.OK

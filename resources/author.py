from models.book import Author
from flask_restful import Resource
from schemas.book import AuthorSchema, PaginatedAuthorSchema
from http import HTTPStatus
from flask_jwt_extended import jwt_required
from webargs import fields
from webargs.flaskparser import use_kwargs
from sqlalchemy import asc, desc
from extension import cache


class AuthorCollectionResource(Resource):
    @jwt_required()
    @use_kwargs(
        {
            "page": fields.Integer(missing=1),
            "per_page": fields.Integer(missing=5),
            "order": fields.String(missing="asc"),
            "sort": fields.String(missing="id"),
            "q": fields.String(missing="")
        }, location="querystring")
    @cache.cached(query_string=True)
    def get(self, page, per_page, order, sort, q):
        keyword = f"%{q}%"
        if sort not in ["id", "name"]:
            sort = "id"
        if order != "desc":
            sort_logic = asc(getattr(Author, sort))
        else:
            sort_logic = desc(getattr(Author, sort))
        authors = Author.query.filter(Author.name.ilike(keyword)).order_by(sort_logic).paginate(page=page,
                                                                                                per_page=per_page)
        return PaginatedAuthorSchema().dump(authors), HTTPStatus.OK


class AuthorResource(Resource):
    @jwt_required()
    @cache.cached()
    def get(self, author_id):
        author = Author.query.filter_by(id=author_id).first()
        if not author:
            return {"message": "Author not found!"}, HTTPStatus.NOT_FOUND
        return AuthorSchema(exclude=["id"]).dump(author), HTTPStatus.OK

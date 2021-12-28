from flask_restful import Resource
from flask_jwt_extended import jwt_required
from http import HTTPStatus
from models.book import Category
from schemas.book import CategoryCollectionSchema, CategorySchema


class CategoryCollectionResource(Resource):
    @jwt_required()
    def get(self):
        categories = Category.query.all()
        return CategoryCollectionSchema(many=True).dump(categories), HTTPStatus.OK


class CategoryResource(Resource):
    @jwt_required()
    def get(self, category_id):
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            return {"message": "Category not found!"}, HTTPStatus.NOT_FOUND

        return CategorySchema(exclude=["id"]).dump(category), HTTPStatus.OK

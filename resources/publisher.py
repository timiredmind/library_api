from flask_restful import Resource
from models.book import Publisher
from flask_jwt_extended import jwt_required
from schemas.book import PublisherCollectionSchema, PublisherSchema
from http import HTTPStatus


class PublisherCollectionResource(Resource):
    @jwt_required()
    def get(self):
        publishers = Publisher.query.all()
        return PublisherCollectionSchema(many=True).dump(publishers), HTTPStatus.OK


class PublisherResource(Resource):
    @jwt_required()
    def get(self, publisher_id):
        publisher = Publisher.query.filter_by(id=publisher_id).first()
        if not publisher:
            return {"message": "Publisher not found!"}, HTTPStatus.NOT_FOUND
        return PublisherSchema().dump(publisher), HTTPStatus.OK

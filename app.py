from extension import db, migrate, jwt, cache, limiter
from models.blocklist import TokenBlockList
from flask import Flask, request
from config import Config, TestingConfig
from flask_restful import Api
from resources.user import CreateUserResource, UserLoginResource, UserProfileResource, UserLogoutResource
from resources.book import BookCollectionResource, BookResource, BorrowBookResource, ReturnBookResource
from resources.author import AuthorCollectionResource, AuthorResource
from resources.publisher import PublisherCollectionResource, PublisherResource
from resources.category import CategoryResource, CategoryCollectionResource
from resources.admin import AdminUsersCollectionResource, AdminUsersResource, AdminBooksCollectionResource, \
    AdminBookResource, AdminAuthorCollectionResource, AdminAuthorResource, AdminPublisherCollectionResource, \
    AdminPublisherResource, AdminCategoriesCollectionResource, AdminCategoryResource, CreateAdminUserResource


def register_extensions(app):
    # Initialize database setup
    db.init_app(app)
    # Initialize migration extension
    migrate.init_app(app, db)
    # Initialize Flask-JWT-Extended extension
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)


def register_resources(app):
    api = Api(app)
    api.add_resource(CreateUserResource, "/users/register")
    api.add_resource(UserLoginResource, "/login")
    api.add_resource(UserLogoutResource, "/logout")
    api.add_resource(UserProfileResource, "/users/profile")
    api.add_resource(BookCollectionResource, "/books")
    api.add_resource(BookResource, "/books/<int:book_id>")
    api.add_resource(AuthorCollectionResource, "/authors")
    api.add_resource(AuthorResource, "/authors/<int:author_id>")
    api.add_resource(PublisherCollectionResource, "/publishers")
    api.add_resource(PublisherResource, "/publishers/<int:publisher_id>")
    api.add_resource(CategoryCollectionResource, "/categories")
    api.add_resource(CategoryResource, "/categories/<int:category_id>")
    api.add_resource(BorrowBookResource, "/books/<int:book_id>/borrow")
    api.add_resource(ReturnBookResource, "/books/<int:book_id>/return")
    api.add_resource(CreateAdminUserResource, "/admin/register")
    api.add_resource(AdminUsersCollectionResource, "/admin/users")
    api.add_resource(AdminUsersResource, "/admin/users/<int:user_id>")
    api.add_resource(AdminBooksCollectionResource, "/admin/books")
    api.add_resource(AdminBookResource, "/admin/books/<int:book_id>")
    api.add_resource(AdminAuthorCollectionResource, "/admin/authors")
    api.add_resource(AdminAuthorResource, "/admin/authors/<int:author_id>")
    api.add_resource(AdminPublisherCollectionResource, "/admin/publishers")
    api.add_resource(AdminPublisherResource,
                     "/admin/publishers/<int:publisher_id>")
    api.add_resource(AdminCategoriesCollectionResource, "/admin/category")
    api.add_resource(
        AdminCategoryResource,
        "/admin/category/<int:category_id>")


def create_app(env="development"):
    # Create an instance of Flask application
    app = Flask(__name__)
    # Load configurations from the Config class
    if env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    # Ease rate limit for requests from ip address 127.0.0.1 or localhost
    @limiter.request_filter
    def ip_whitelist():
        return request.remote_addr == "127.0.0.1"

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlockList).filter_by(jti=jti).scalar()
        return token is not None
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

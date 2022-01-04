from extension import db, migrate, jwt
from flask import Flask, url_for
from config import Config
from flask_restful import Api
from resources.user import CreateUserResource, UserLoginResource, UserProfileResource, UserActivationResource
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


def register_resources(app):
    api = Api(app)
    api.add_resource(CreateUserResource, "/users/register")
    api.add_resource(UserLoginResource, "/login")
    api.add_resource(UserProfileResource, "/users/profile")
    api.add_resource(UserActivationResource, "/users/activate/<string:token>")
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
    api.add_resource(AdminPublisherResource, "/admin/publishers/<int:publisher_id>")
    api.add_resource(AdminCategoriesCollectionResource, "/admin/category")
    api.add_resource(AdminCategoryResource, "/admin/category/<int:category_id>")


def create_app():
    # Create an instance of Flask application
    app = Flask(__name__)
    # Load configurations from the Config class
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

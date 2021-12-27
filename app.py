from extension import db, migrate, jwt
from flask import Flask
from config import Config
from flask_restful import Api
from resources.user import CreateUserResource, UserLoginResource, UserProfileResource
from resources.book import BookCollectionResource, BookResource
from models.user import User
from utils import hash_password


def register_extensions(app):
    # Initialize database setup
    db.init_app(app)
    # Initialize migration extension
    migrate.init_app(app, db)
    # Initialize Flask-JWT-Extended extension
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)
    api.add_resource(CreateUserResource, "/register")
    api.add_resource(UserLoginResource, "/login")
    api.add_resource(UserProfileResource, "/users/profile")
    api.add_resource(BookCollectionResource, "/books")
    api.add_resource(BookResource, "/books/<int:book_id>")


def create_app():
    # Create an instance of Flask application
    app = Flask(__name__)
    # Load configurations from the Config class
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    @app.cli.command("create-admin-user")
    def create_admin_user():
        if User.check_username("admin"):
            print("Admin user already exists.")
        else:
            username = "admin"
            password = hash_password("admin")
            email = "joshua_oladokun@gmail.com"
            role = "admin"
            admin_user = User(username=username, password=password, email=email, role=role)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully, the admin username is 'admin' and password is 'admin'")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

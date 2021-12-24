from extension import db, migrate
from flask import Flask
from config import Config

# Create an instance of Flask application
app = Flask(__name__)
# Load configurations from the Config class
app.config.from_object(Config)
# Initialize database setup
db.init_app(app)
# Initialize migration extension
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run()

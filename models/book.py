from extension import db


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    description = db.Column(db.String)
    books = db.relationship("Book", backref="author")


class Publisher(db.Model):
    __tablename__ = "publishers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True, unique=True)
    books = db.relationship("Book", backref="publisher")


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship("Book", backref="category")


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    num_of_pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    isbn13 = db.Column(db.String, nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id", ondelete="CASCADE"))
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id", ondelete="CASCADE"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"))
    date_donated = db.Column(db.DateTime, default=db.func.now())
    cover_url = db.Column(db.String)
    is_available = db.Column(db.Boolean, default=True)
    book_loan_history = db.relationship("BooksBorrowed", backref="book")
    language = db.Column(db.String, nullable=False)


class BooksBorrowed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)
    date_borrowed = db.Column(db.DateTime, default=db.func.now())
    date_returned = db.Column(db.DateTime)
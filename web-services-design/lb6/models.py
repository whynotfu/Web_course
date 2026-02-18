import os
from datetime import datetime

from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = "categories"

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    courses = db.relationship("Course", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    login         = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return " ".join(p for p in [self.first_name, self.last_name] if p)

    def __repr__(self):
        return f"<User {self.login}>"


class Image(db.Model):
    __tablename__ = "images"

    id        = db.Column(db.String(36), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100))
    md5_hash  = db.Column(db.String(32), unique=True, nullable=False)

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return f"{self.id}{ext}"

    @property
    def url(self):
        return url_for('image', image_id=self.id)

    def __repr__(self):
        return f"<Image {self.id}>"


class Course(db.Model):
    __tablename__ = "courses"

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(200), nullable=False)
    short_desc          = db.Column(db.Text)
    full_desc           = db.Column(db.Text)
    rating_sum          = db.Column(db.Integer, default=0, nullable=False)
    rating_num          = db.Column(db.Integer, default=0, nullable=False)
    category_id         = db.Column(db.Integer, db.ForeignKey("categories.id"))
    author_id           = db.Column(db.Integer, db.ForeignKey("users.id"))
    background_image_id = db.Column(db.String(36), db.ForeignKey("images.id"))
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)

    author   = db.relationship("User", backref="courses",
                               foreign_keys="[Course.author_id]")
    bg_image = db.relationship("Image",
                               foreign_keys="[Course.background_image_id]")
    themes   = db.relationship("Theme", backref="course", lazy=True,
                               cascade="all, delete-orphan")
    reviews  = db.relationship("Review", backref="course", lazy=True,
                               cascade="all, delete-orphan")

    @property
    def rating(self):
        if self.rating_num == 0:
            return None
        return round(self.rating_sum / self.rating_num, 1)

    def __repr__(self):
        return f"<Course {self.name}>"


class Theme(db.Model):
    __tablename__ = "themes"

    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(200), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    subthemes = db.relationship("SubTheme", backref="theme", lazy=True,
                                cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Theme {self.name}>"


class SubTheme(db.Model):
    __tablename__ = "subthemes"

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(200), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey("themes.id"))

    def __repr__(self):
        return f"<SubTheme {self.name}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id         = db.Column(db.Integer, primary_key=True)
    rating     = db.Column(db.Integer, nullable=False)
    text       = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    course_id  = db.Column(db.Integer, db.ForeignKey("courses.id"))
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="reviews")

    RATING_LABELS = {
        5: "Отлично",
        4: "Хорошо",
        3: "Удовлетворительно",
        2: "Неудовлетворительно",
        1: "Плохо",
        0: "Ужасно",
    }

    @property
    def rating_label(self):
        return self.RATING_LABELS.get(self.rating, str(self.rating))

    def __repr__(self):
        return f"<Review {self.id} rating={self.rating}>"

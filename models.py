from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

db = SQLAlchemy()


# =========================================================
# User
# =========================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    todos = db.relationship(
        "Todo",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    diaries = db.relationship(
        "Diary",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    schedules = db.relationship(
        "Schedule",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = (
            generate_password_hash(password)
        )

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


# =========================================================
# Todo
# =========================================================

class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text
    )

    due_date = db.Column(
        db.Date
    )

    priority = db.Column(
        db.String(20),
        default="NORMAL"
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )


# =========================================================
# Diary
# =========================================================

class Diary(db.Model):
    __tablename__ = "diaries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    mood = db.Column(
        db.String(30)
    )

    happiness_score = db.Column(
        db.Integer
    )

    diary_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )


# =========================================================
# Schedule
# =========================================================

class Schedule(db.Model):
    __tablename__ = "schedules"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text
    )

    start_datetime = db.Column(
        db.DateTime,
        nullable=False
    )

    end_datetime = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )


# =========================================================
# Important Diary
# =========================================================

class ImportantDiary(db.Model):
    __tablename__ = "important_diaries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    diary_id = db.Column(
        db.Integer,
        db.ForeignKey("diaries.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "diary_id",
            name="uq_important_diary_user"
        ),
    )
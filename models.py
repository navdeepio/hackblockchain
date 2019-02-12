from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class JobType(Enum):
    contract = 'Contract'
    full_time = 'Full Time'
    part_time = 'Part Time'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    jobs = db.relationship('Job', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, unique=True, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.email


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    link_to_apply = db.Column(db.String(300), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_location = db.Column(db.String(100))
    company_name = db.Column(db.String(100), nullable=False)
    company_url = db.Column(db.String(300), nullable=False)
    job_type = db.Column(db.Enum(JobType), nullable=False)
    remote_ok = db.Column(db.Boolean, nullable=False, default=False)


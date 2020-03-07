from api import db
from passlib.apps import custom_app_context as pwd_context
from api import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import g


class User(db.Model):
    __tablename__ = "apiuser"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    task = db.relationship('Task', backref='apiuser', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Task(db.Model):
    __tablename__ = "TaskList"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(64))
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("apiuser.id"))

    def __init__(self, args):
        self.content = args['content']
        self.done = args['done']
        self.begin_time = args['begin_time']
        self.end_time = args['end_time']
        self.user_id = g.user.id

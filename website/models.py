from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(150))
    buy = db.Column(db.Float)
    sell = db.Column(db.Float)
    fees = db.Column(db.Float)
    profit = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    profitPercent = db.Column(db.Float)
    roi = db.Column(db.Float)
    roiPercent = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    trades = db.relationship('Trade')
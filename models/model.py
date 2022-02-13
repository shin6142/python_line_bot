from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_FIXED') or 'sqlite:///calender.db'
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    stamps = relationship("Stamp")


class Stamp(db.Model):
    
    __tablename__ = 'stamp'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def add_user(username):
    if username != 'favicon.ico':
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()

def add_stamp(user_id: int):
    new_stamp = Stamp(user_id=user_id)
    db.session.add(new_stamp)
    db.session.commit()

def get_user(user_id):
    user = db.session.query(User).filter(User.id==user_id).first()
    return user

def get_user_by_name(username):
    user = db.session.query(User).filter(User.username==username).first()
    return user

def get_check_in_date_list(user_id):
    stamps = db.session.query(Stamp).\
        filter(Stamp.user_id == user_id).all()
    check_in_date_list = []
    for stamp in stamps:
        check_in_date_list.append(stamp.created_at)
    return check_in_date_list

def get_monthly_date_list(user_id):
    check_in_date_list = get_check_in_date_list(user_id)
    import datetime
    dt_now = datetime.datetime.now()
    monthly_date_list = []
    for date in check_in_date_list:
        if date.year==dt_now.year and date.month==dt_now.month:
            monthly_date_list.append(date.day)
    unique_date_list = list(dict.fromkeys(monthly_date_list))
    return unique_date_list
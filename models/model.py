from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///calender.db'
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

def get_user(username):
    user = db.session.query(User).filter(User.username==username).first()
    return user

# if __name__ == "__main__":
#     app.run()


# db.drop_all()
# db.create_all()

# for user in users:
#     print(user.username, user.id)
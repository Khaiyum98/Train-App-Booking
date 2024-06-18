from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    departure_time = db.Column(db.String(20), nullable=False)
    arrival_time = db.Column(db.String(20), nullable=False)
    coaches = db.relationship('Coach', backref='train', lazy=True)

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coach_number = db.Column(db.String(10), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    seats = db.relationship('Seat', backref='coach', lazy=True)

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)

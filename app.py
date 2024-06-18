from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///train_ticket_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route('/')
def index():
    trains = Train.query.all()
    return render_template('index.html', trains=trains)

@app.route('/book/<train_id>/<coach_id>', methods=['GET', 'POST'])
def book(train_id, coach_id):
    coach = Coach.query.get_or_404(coach_id)
    if request.method == 'POST':
        seat_number = int(request.form['seat'])
        seat = Seat.query.filter_by(coach_id=coach_id, seat_number=seat_number).first()
        if seat and not seat.is_booked:
            seat.is_booked = True
            db.session.commit()
            return redirect(url_for('summary', train_id=train_id, coach_id=coach_id, seat_number=seat_number))
    seats = Seat.query.filter_by(coach_id=coach_id).all()
    return render_template('booking.html', train_name=coach.train.name, coach_name=coach.coach_number, seats=seats)

@app.route('/summary/<train_id>/<coach_id>/<int:seat_number>')
def summary(train_id, coach_id, seat_number):
    train = Train.query.get_or_404(train_id)
    coach = Coach.query.get_or_404(coach_id)
    return render_template('summary.html', train=train, coach_name=coach.coach_number, seat_number=seat_number)

if __name__ == '__main__':
    app.run(debug=True)

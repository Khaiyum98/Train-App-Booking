from app import app, db, Train, Coach, Seat

with app.app_context():
    # Create all tables
    db.create_all()

    # Sample data initialization
    if not Train.query.first():
        train = Train(name='Train1', departure_time='10:00 AM', arrival_time='02:00 PM')
        db.session.add(train)
        db.session.commit()
        for i in range(6):
            coach = Coach(coach_number=f'Coach{i+1}', train_id=train.id)
            db.session.add(coach)
            db.session.commit()
            for j in range(20):
                seat = Seat(seat_number=j+1, coach_id=coach.id)
                db.session.add(seat)
                db.session.commit()

    print("Database initialized successfully.")

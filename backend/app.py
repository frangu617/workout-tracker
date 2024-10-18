from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    age = db.Column(db.Integer)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workout_type = db.Column(db.String(50))
    workout_name = db.Column(db.String(100))
    duration = db.Column(db.Float)  # for cardio workouts
    sets = db.Column(db.Integer)    # for weight training and bodyweight workouts
    reps = db.Column(db.Integer)    # for weight training and bodyweight workouts
    weight = db.Column(db.Float)    # for weight training

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], height=data['height'], weight=data['weight'], age=data['age'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'})

@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = Workout(
        user_id=data['user_id'],
        workout_type=data['workout_type'],
        workout_name=data.get('workout_name'),
        duration=data.get('duration'),
        sets=data.get('sets'),
        reps=data.get('reps'),
        weight=data.get('weight')
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': 'Workout added successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'height': user.height,
            'weight': user.weight,
            'age': user.age
        }
        users_list.append(user_data)
    return jsonify( users_list)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = {
            'id': user.id,
            'name': user.name,
            'height': user.height,
            'weight': user.weight,
            'age': user.age
        }
        return jsonify(user_data)
    else:
        return jsonify({'message': 'User not found'})
    
    
@app.route('/edit_user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.name = data.get('name', user.name)
        user.height = data.get('height', user.height)
        user.weight = data.get('weight', user.weight)
        user.age = data.get('age', user.age)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

    
    
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

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

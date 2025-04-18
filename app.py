from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import googlemaps
import tensorflow as tf
from datetime import datetime

#model = tf.keras.models.load_model('my_traffic_model.keras') 

# Load the trained LSTM model
model = tf.keras.models.load_model('traffic_prediction_model23.h5')


print("Model loaded successfully!")

app = Flask(__name__, template_folder="template")  # Ensure the folder is named 'template'

app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# Google Maps API Key
gmaps = googlemaps.Client(key='AIzaSyBMI1ndJMecoaZLA5wMYl5eDZXbUOjzjs8')


# Load trained model
#model = tf.keras.models.load_model("traffic_prediction_model2.keras")

# User Model (Updated to match SQL Schema correctly)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Added username
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)



# Route: Home (Login/Register)
@app.route('/')
def home():
    return render_template('login.html')

# Route: Register
#@app.route('/register', methods=['GET', 'POST'])
#def register():
#    if request.method == 'POST':
#        email = request.form['email']
#        password = generate_password_hash(request.form['password'])
#        new_user = User(email=email, password=password)
#        db.session.add(new_user)
#        db.session.commit()
#        return redirect(url_for('home'))
#    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate input
        if not username or not email or not password:
            return "Missing username, email, or password!"

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return f"Database error: {e}"

    return render_template('register.html')


# Route: Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user'] = user.email
        return redirect(url_for('index'))
    return 'Invalid credentials!'

# Route: Index (Prediction Input)
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        time = request.form['time']
        weekday = request.form['weekday']
        return redirect(url_for('result', origin=origin, destination=destination, time=time, weekday=weekday))
    return render_template('index.html')

# Route: Result (Prediction & Traffic Suggestion)
# Mapping weekday names to numbers
weekday_mapping = {
    'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
    'Friday': 4, 'Saturday': 5, 'Sunday': 6
}


@app.route('/result')
def result():
    if 'user' not in session:
        return redirect(url_for('home'))

    origin = request.args.get('origin')
    destination = request.args.get('destination')
    time_str = request.args.get('time')  # "HH:MM" format
    weekday_str = request.args.get('weekday')  # Example: "Tuesday"

    # Convert time to minutes since midnight
    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        time_in_minutes = time_obj.hour * 60 + time_obj.minute  
    except:
        return "Invalid time format. Use HH:MM", 400

    # Convert weekday string to numerical value
    weekday_num = weekday_mapping.get(weekday_str, -1)  # -1 for error checking
    if weekday_num == -1:
        return "Invalid weekday", 400

    # LSTM Model Input
    time_step = 10
    features = [time_in_minutes, weekday_num, 0, 0, 0]
    sequence_input = np.array([features] * time_step)  # Shape: (10, 5)
    sequence_input = np.expand_dims(sequence_input, axis=0)  # Final shape: (1, 10, 5)

    # Model Prediction
    traffic_prediction = model.predict(sequence_input)[0][0]  # Get single float value

    # Categorize traffic level based on prediction value
    if traffic_prediction < 0.3:
        congestion_level = "Low"
    elif traffic_prediction < 0.7:
        congestion_level = "Medium"
    else:
        congestion_level = "High"

    # Get route using Google Maps API
    directions = gmaps.directions(origin, destination, departure_time='now')

    # Extract distance in km if available
    predicted_distance = None
    if directions:
        try:
            predicted_distance = directions[0]['legs'][0]['distance']['text'].replace(" km", "")
        except:
            predicted_distance = "N/A"

    return render_template('result.html',
                           congestion_level=congestion_level,
                           predicted_distance=predicted_distance,
                           origin=origin,
                           destination=destination,
                           time=time_str)

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

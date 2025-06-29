from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendee = db.Column(db.String(100))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Add/View Events Page
@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        event = Event(name=name, location=location)
        db.session.add(event)
        db.session.commit()
        return redirect('/events')

    events = Event.query.all()
    return render_template('events.html', events=events)

# Register Page (with message)
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        event_id = request.form['event']
        reg = Registration(attendee=name, event_id=event_id)
        db.session.add(reg)
        db.session.commit()
        message = f"✅ {name}, you are registered for this event!"

    events = Event.query.all()
    return render_template('register.html', events=events, message=message)

# Start app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

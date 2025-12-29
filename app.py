from flask import Flask, render_template, request, flash

from models import db
from models.event import Event
from forms import AddEventForm

def create_app():
    app = Flask(__name__)

    # Encrypt traffic between this Flask app and the client
    app.secret_key = 'secretkey'

    # Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Initialize the database
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add_event', methods=['GET', 'POST'])
    def add_event():
        form = AddEventForm()

        if request.method == 'POST':
            new_event = Event(title=form.title.data)
            db.session.add(new_event)

            try:
                db.session.commit()
                flash('Added event', 'success')
            except Exception as e:
                flash(str(e), 'danger')

            events = Event.query.all()

            return render_template('events.html', events=events)

        return render_template('add_event_form.html', form=form, page_title='Add Event')


    # Return the flask application
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


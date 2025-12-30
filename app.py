from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from extensions import db
from models.event import Event
from forms import AddEventForm, UpdateEventForm

def create_app(testing=False):
    app = Flask(__name__)

    # Encrypt traffic between this Flask app and the client
    app.secret_key = 'secretkey'

    # Use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///:memory:' if testing else 'sqlite:///community.db'
    )
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

        if request.method == 'POST' and form.validate_on_submit():
            new_event = Event(title=form.title.data)
            db.session.add(new_event)

            try:
                db.session.commit()
                flash('Added event', 'success')
            except IntegrityError:
                flash('Eent name must be unique!', 'danger')
                db.session.rollback()
            except Exception as e:
                flash(str(e), 'danger')

            events = Event.query.all()
            return render_template('events.html', events=events)

        return render_template('add_event_form.html', form=form, page_title='Add Event')

    @app.route('/list_events')
    def list_events():
        events = Event.query.all()

        return render_template('events.html', events=events)

    @app.route('/event_action', methods=['POST'])
    def event_action():

        event_id = request.form.get('event_id')
        action = request.form.get('action')

        if not event_id:
            flash('Please select an event', 'warning')
            return redirect(url_for('list_events'))
        
        if action == 'update':
            return redirect(url_for('update_event', id=event_id))
        elif action == 'delete':
            return redirect(url_for('delete_event', id=event_id))
        else:
            flash('Invalid action', 'danger')
            return redirect(url_for('list_events'))

    @app.route('/update_event/<int:id>', methods=['GET', 'POST'])
    def update_event(id):
        event = Event.query.get_or_404(id)

        form = UpdateEventForm(obj=event)

        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(event)

            try:
                db.session.commit()
                flash('Event updated', 'success')
                return redirect(url_for('list_events'))
            except IntegrityError:
                flash('Event name must be unique!', 'danger')
                db.session.rollback()
        else:
            print('Something happened')
        
        return render_template('update_event_form.html', 
            form=form, page_title='Update event')


    @app.route('/delete_event/<int:id>')
    def delete_event(id):
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        
        flash('Event deleted', 'success')
        return redirect(url_for('list_events')) 

    # Return the flask application
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


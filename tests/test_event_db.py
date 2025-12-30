from extensions import db
from models.event import Event
from datetime import date

from app import create_app

def test_event_persistence():
    """
    GIVEN a Event model
    WHEN a new Event is saved to the database
    THEN check the title is saved correctly
    """

    app = create_app(testing=True)

    with app.app_context():
        db.create_all()

        event = Event(title='Test Event', date=date(2026, 8, 5))
        db.session.add(event)
        db.session.commit()

        saved_event = Event.query.first()

        assert saved_event is not None
        assert saved_event.title == 'Test Event'
        assert event.date == date(2026, 8, 5)
from datetime import date, time
from models.event import Event

def test_new_event():
    """
    GIVEN a Event model
    WHEN a new Event is created
    THEN check the title is defined correctly
    """

    event = Event(title='New Event', 
        date=date(2025, 12, 10), time=time(hour=10, minute=15, second=33))
    assert event.title == 'New Event'
    assert event.date == date(2025, 12, 10)
    assert event.time == time(hour=10, minute=15, second=33)
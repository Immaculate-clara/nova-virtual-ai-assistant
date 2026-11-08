"""Date and time reporting using the datetime module (FR-03, FR-04)."""
from datetime import datetime


def get_current_time(now=None):
    """e.g. "It's currently 3:45 PM." (`now` lets tests pass a fixed time)."""
    now = now or datetime.now()
    return "It's currently " + now.strftime("%I:%M %p").lstrip("0") + "."


def get_current_date(now=None):
    """e.g. "Today's date is Saturday, 07 November 2026."."""
    now = now or datetime.now()
    return "Today's date is " + now.strftime("%A, %d %B %Y") + "."

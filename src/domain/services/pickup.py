from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from domain.constants import MIN_DAYS_BEFORE_PICKUP


def earliest_pickup_date() -> date:
    today = datetime.now(ZoneInfo("Europe/Minsk")).date()
    return today + timedelta(days=MIN_DAYS_BEFORE_PICKUP)

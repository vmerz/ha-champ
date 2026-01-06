from datetime import date, datetime
from typing import Optional


def calculate_age(birthdate_str: Optional[str]) -> Optional[int]:
    """Calculate age from birthdate string (YYYY-MM-DD).

    Returns:
        Age in years, or None if no birthdate provided.
    """
    if not birthdate_str:
        return None

    try:
        birthdate = datetime.fromisoformat(birthdate_str).date()
        today = date.today()

        age = today.year - birthdate.year

        # Adjust if birthday hasn't occurred this year yet
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1

        return age
    except (ValueError, AttributeError):
        return None

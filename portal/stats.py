from datetime import date, timedelta

def get_period_range(period_offset, period_length):
    """
    Get the start date and end date of a period (week, month, quarter, or year) based on the current date.
    :param period_offset: Number of periods to offset from the current period (negative for past, positive for future).
    :param period_length: Type of period ("weeks", "months", "quarters", or "years").
    :return: A dictionary with 'start_date' and 'end_date'.
    """
    today = date.today()
    
    if period_length == "weeks":
        # For weeks, start on Sunday and end on Saturday
        start_of_current_period = today - timedelta(days=today.weekday() + 1)  # Monday is 0, Sunday is 6
        start_of_period = start_of_current_period + timedelta(weeks=period_offset)
        end_of_period = start_of_period + timedelta(days=6)
    elif period_length == "months":
        # For months, start on the first day and end on the last day
        year = today.year
        month = today.month + period_offset
        # Handle year overflow/underflow
        while month > 12:
            month -= 12
            year += 1
        while month < 1:
            month += 12
            year -= 1
        start_of_period = date(year, month, 1)
        # Calculate the last day of the month
        if month == 12:
            end_of_period = date(year, month, 31)
        else:
            end_of_period = date(year, month + 1, 1) - timedelta(days=1)
    elif period_length == "quarters":
        # For quarters, start on the first day of the quarter and end on the last day
        current_quarter = (today.month - 1) // 3 + 1  # Calculate current quarter (1-4)
        start_month = 3 * (current_quarter - 1) + 1  # First month of the current quarter
        year = today.year
        start_month += 3 * period_offset
        # Handle year overflow/underflow
        while start_month > 12:
            start_month -= 12
            year += 1
        while start_month < 1:
            start_month += 12
            year -= 1
        start_of_period = date(year, start_month, 1)
        # Calculate the last day of the quarter
        end_month = start_month + 2  # Last month of the quarter
        if end_month > 12:
            end_month -= 12
            year += 1
        # Calculate the last day of the last month in the quarter
        if end_month == 12:
            end_of_period = date(year, end_month, 31)
        else:
            end_of_period = date(year, end_month + 1, 1) - timedelta(days=1)
    elif period_length == "years":
        # For years, start on the first day and end on the last day
        year = today.year + period_offset
        start_of_period = date(year, 1, 1)
        end_of_period = date(year, 12, 31)
    else:
        raise ValueError("Invalid period_length. Use 'weeks', 'months', 'quarters', or 'years'.")
    
    return {
        'start_date': start_of_period,
        'end_date': end_of_period
    }

def generate_periods(past_offset=7, future_offset=2, period_length="months"):
    """
    Generate a list of periods: past periods, current period, and future periods.
    :param past_offset: Number of past periods to include.
    :param future_offset: Number of future periods to include.
    :param period_length: Type of period ("weeks", "months", "quarters", or "years").
    :return: List of period objects with 'label', 'start_date' 'end_date', and 'units'.
    """
    periods = []
    for period_offset in range(-past_offset, future_offset + 1):  # From past_offset periods ago to future_offset periods ahead
        period_range = get_period_range(period_offset, period_length)
        
        # Generate a label based on the period length
        if period_length == "weeks":
            # label = f"W{period_range['start_date'].isocalendar()[1]:02d} {period_range['start_date'].strftime("%y")}"  # ISO week number
            label = period_range['start_date'].strftime("%d %b")  # Week start date (09 Jan)
        elif period_length == "months":
            label = period_range['start_date'].strftime("%b %y")  # Month abbreviation and year
        elif period_length == "quarters":
            quarter_number = (period_range['start_date'].month - 1) // 3 + 1  # Quarter number (1-4)
            label = f"Q{quarter_number} {period_range['start_date'].strftime("%y")}"  # Quarter and year
        elif period_length == "years":
            label = str(period_range['start_date'].year)  # Year
        else:
            raise ValueError("Invalid period_length. Use 'weeks', 'months', 'quarters', or 'years'.")
        periods.append({
            'label': label,
            'start_date': period_range['start_date'],
            'end_date': period_range['end_date'],
            'units': period_length,
        })
    return periods


example_data = [
        {
            "Aug 24": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [187622892.64, 310653160.61, 1290945206.41]
                }
            ]
            }
        },
        {
            "Sep 24": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [1970532780.61, 2331566647.82, 7106840598.47]
                }
            ]
            }
        },
        {
            "Oct 24": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [2542355630.57, 2984428848.22, 7488477030.24]
                }
            ]
            }
        },
        {
            "Nov 24": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [3253394040.75, 6527388956.55, 19127899190.18]
                }
            ]
            }
        },
        {
            "Dec 24": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [3102940859.58, 3252994539.65, 11271652154.47]
                }
            ]
            }
        },
        {
            "Jan 25": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [4612155969.43, 2539561990.46, 5721948436.94]
                }
            ]
            }
        },
        {
            "Feb 25": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [4304638114.74, 1599350334.18, 7064473325.69]
                }
            ]
            }
        },
        {
            "Mar 25": {
            "labels": ["Fournitures", "Services", "Travaux"],
            "datasets": [
                {
                "data": [632004816.0, 276606510.24, 1336064648.99]
                }
            ]
            }
        }
    ]

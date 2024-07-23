from datetime import datetime, timedelta
def get_current_week():
    start_week = (datetime.now() - timedelta(days=datetime.now().weekday()))
    end_week = start_week + timedelta(days=6)
    return start_week, end_week

def get_current_time():
    return datetime.now()

def get_last_week_time():
    return datetime.now() - timedelta(days=7)

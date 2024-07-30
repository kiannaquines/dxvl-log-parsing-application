from datetime import datetime, timedelta
from django.utils import timezone

def get_current_week():
    start_week = timezone.make_aware((datetime.now() - timedelta(days=datetime.now().weekday())))
    end_week = timezone.make_aware(start_week + timedelta(days=6))
    return start_week, end_week

def get_current_time():
    return timezone.make_aware(datetime.now())

def get_last_week_time():
    return timezone.make_aware(datetime.now() - timedelta(days=7))

def get_week_range(week_str):
    year, week = map(int, week_str.split('-W'))
    first_day_of_week = timezone.make_aware(datetime.strptime(f'{year}-W{week}-1', "%Y-W%W-%w").date())
    last_day_of_week = timezone.make_aware(first_day_of_week + timedelta(days=6))
    return first_day_of_week, last_day_of_week

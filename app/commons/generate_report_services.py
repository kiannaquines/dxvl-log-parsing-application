from xhtml2pdf import pisa
from app.models import DXVLLogs
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('login'))
def generate_monthly_report(start_month, end_month):
    pass

@login_required(login_url=reverse_lazy('login'))
def generate_weekly_report(start_week, end_week):
    pass

@login_required(login_url=reverse_lazy('login'))
def generate_daily_report(start_date, end_date):
    pass
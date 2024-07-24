from xhtml2pdf import pisa
from app.models import DXVLLogs
from app.commons.common_services import filter_objects, filter_objects_count
from datetime import datetime
from dxvl.settings import BASE_DIR
from django.template.loader import get_template
from django.http import HttpResponse


def generate_daily_report(start_date, end_date, response):
    count_check = filter_objects_count(
        DXVLLogs.objects, date_aired__range=(start_date, end_date)
    )

    template_pdf = get_template("pdf_template/template.html")
    context = {}

    if count_check == 0:
        return "no_logs_found"

    daily_logs = filter_objects(
        DXVLLogs.objects, date_aired__range=(start_date, end_date)
    )

    context["daily_logs"] = daily_logs
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")

    rendered = template_pdf.render(context)
    createPDF = pisa.CreatePDF(rendered, dest=response)

    if createPDF.err:
        return "error_in_parsing_pdf"

    return createPDF


def generate_monthly_report(start_month, end_month):
    pass


def generate_weekly_report(start_week, end_week):
    pass

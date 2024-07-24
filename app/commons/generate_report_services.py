from xhtml2pdf import pisa
from app.models import DXVLLogs
from app.commons.common_services import filter_objects, filter_objects_count
from datetime import datetime
from dxvl.settings import BASE_DIR
from django.template.loader import get_template
import os
from django.db.models import F, Value, CharField, Case, When
from django.db.models.functions import Concat, Extract, Length


def generate_daily_report(date, response):
    count_check = filter_objects_count(
        DXVLLogs.objects,
        date_aired__date=date,
    )

    template_pdf = get_template("pdf_template/template.html")
    context = {}

    if count_check == 0:
        return "no_logs_found"

    daily_logs = (
        DXVLLogs.objects.filter(date_aired__date=date)
        .annotate(
            day=Extract("date_aired", "day"),
            month=Extract("date_aired", "month"),
            year=Extract("date_aired", "year"),
            hour=Extract("date_aired", "hour"),
            minute=Extract("date_aired", "minute"),
            second=Extract("date_aired", "second"),
        )
        .annotate(
            month_padded=Case(
                When(
                    month__lt=10,
                    then=Concat(Value("0"), F("month"), output_field=CharField()),
                ),
                default=F("month"),
                output_field=CharField(),
            ),
            day_padded=Case(
                When(
                    day__lt=10,
                    then=Concat(Value("0"), F("day"), output_field=CharField()),
                ),
                default=F("day"),
                output_field=CharField(),
            ),
            minute_padded=Case(
                When(
                    minute__lt=10,
                    then=Concat(
                        Value("0"),
                        F("minute"),
                        output_field=CharField(),
                    ),
                ),
                default=F("minute"),
                output_field=CharField(),
            ),
            second_padded=Case(
                When(
                    second__lt=10,
                    then=Concat(
                        Value("0"),
                        F("second"),
                        output_field=CharField(),
                    ),
                ),
                default=F("second"),
                output_field=CharField(),
            ),
            remarks_padded=Case(
                When(remarks=True, then=Value("Aired")),
                When(remarks=False, then=Value("Unaired")),
                default=Value("Unknown"),
                output_field=CharField(),
            ),
        )
        .annotate(
            formatted_date=Concat(
                F("month_padded"),
                Value("/"),
                F("day_padded"),
                Value("/"),
                F("year"),
                output_field=CharField(),
            ),
            formatted_time=Concat(
                F("hour"),
                Value(":"),
                F("minute_padded"),
                Value(":"),
                F("second_padded"),
                output_field=CharField(),
            ),
        )
        .values(
            "formatted_date",
            "formatted_time",
            "artist",
            "advertisement",
            "remarks_padded",
        )
    )

    context["daily_logs"] = daily_logs
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    context["logo_path"] = os.path.join(BASE_DIR, "static/assets/img/icons/logo.png")
    rendered = template_pdf.render(context)
    createPDF = pisa.CreatePDF(rendered, dest=response)

    if createPDF.err:
        return "error_in_parsing_pdf"

    return createPDF


def generate_monthly_report(start_month, end_month):
    pass


def generate_weekly_report(start_week, end_week):
    pass

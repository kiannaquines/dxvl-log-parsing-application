import os
from xhtml2pdf import pisa
from app.models import DXVLLogs
from app.commons.common_services import filter_objects_count, filter_objects
from datetime import datetime
from dxvl.settings import BASE_DIR, MEDIA_ROOT
from django.template.loader import get_template
from django.db.models import F, Value, CharField, Case, When, Count
from django.db.models.functions import Concat, Extract, Lower
from app.utils.utilities import get_week_range
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db.models.functions import TruncDate
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from datetime import datetime


def chunk_generator(total_count, chunk_size):
    start = 0
    while start < total_count:
        end = min(start + chunk_size, total_count)
        yield (start, end)
        start = end


def fetch_chunk(start, end, first_day, last_day):
    return list(
        DXVLLogs.objects.filter(date_aired__gte=first_day, date_aired__lte=last_day)
        .annotate(
            formatted_date=TruncDate("date_aired"),
            formatted_time=Concat(
                Extract("date_aired", "hour"),
                Value(":"),
                Extract("date_aired", "minute"),
                Value(":"),
                Extract("date_aired", "second"),
                output_field=CharField(),
            ),
            remarks_padded=Case(
                When(remarks=True, then=Value("Aired")),
                When(remarks=False, then=Value("Unaired")),
                default=Value("Unknown"),
                output_field=CharField(),
            ),
        )
        .values(
            "formatted_date",
            "formatted_time",
            "artist",
            "advertisement",
            "remarks_padded",
        )[start:end]
    )


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


def generate_weekly_report(request, week):
    context = {}
    first_day_of_week, last_day_of_week = get_week_range(week)

    total_count = DXVLLogs.objects.filter(
        date_aired__gte=first_day_of_week, date_aired__lte=last_day_of_week
    ).count()

    if total_count == 0:
        return "no_logs_found"

    chunk_size = 500
    all_logs = []

    with ThreadPoolExecutor(max_workers=13) as executor:
        future_to_chunk = {
            executor.submit(
                fetch_chunk, start, end, first_day_of_week, last_day_of_week
            ): (start, end)
            for start, end in chunk_generator(total_count, chunk_size)
        }

        for future in as_completed(future_to_chunk):
            chunk_logs = future.result()
            all_logs.extend(chunk_logs)

    context["weekly_logs"] = all_logs
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/template_weekly.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"dxvl_weekly_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename


def generate_monthly_report(request):
    context = {}

    from django.utils import timezone
    from datetime import datetime

    date_from_str = request.POST.get("date_from")
    date_to_str = request.POST.get("date_to")
    advertisement_str = request.POST.get("advertisement_name","").strip()

    datetime_from = timezone.make_aware(datetime.strptime(date_from_str, "%Y-%m-%d"))
    datetime_to = timezone.make_aware(datetime.strptime(date_to_str, "%Y-%m-%d"))
    range_date = (datetime_from, datetime_to)

    total_count = DXVLLogs.objects.filter(
        advertisement__icontains=advertisement_str,
        date_aired__range=range_date,
    )

    if total_count.count() == 0:
        return "no_logs_found"

    grouped_by_date = (
        DXVLLogs.objects.filter(
            date_aired__range=range_date,
            advertisement__icontains=advertisement_str
        )
        .annotate(grouped_date=TruncDate("date_aired"))
        .values("grouped_date", "advertisement","remarks")
        .annotate(no_played=Count("log_id"))
        .order_by("grouped_date")
    )

    final_data = []

    for data in grouped_by_date:
        log = DXVLLogs.objects.filter(
            advertisement=data['advertisement'],
            date_aired__date=data['grouped_date'],
            remarks=data['remarks'],
        )

        final_data.append(log)

    print("==============================") 
    print(final_data)
    print("==============================")

    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/template_monthly.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"monthly_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename

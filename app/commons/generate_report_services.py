import os
from xhtml2pdf import pisa
from app.models import DXVLLogs
from app.commons.common_services import filter_objects_count
from datetime import datetime
from dxvl.settings import BASE_DIR, MEDIA_ROOT
from django.template.loader import get_template
from django.db.models import F, Value, CharField, Case, When, Count
from django.db.models.functions import Concat, Extract
from app.utils.utilities import get_week_range
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db.models.functions import TruncDate, TruncTime
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from datetime import datetime
from django.utils import timezone

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

def generate_daily_report(date, request):
    count_check = filter_objects_count(
        DXVLLogs.objects,
        date_aired__date=date,
    )


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

    context = {}
    context["daily_logs"] = daily_logs
    context["total_ads"] = daily_logs.count()
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")

    html_string = render_to_string("pdf_template/template_daily.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"dxvl_daily_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename

def generate_weekly_overall_report(request, week):
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
    context["total_ads"] = total_count
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

    date_from_str = request.POST.get("date_from")
    date_to_str = request.POST.get("date_to")
    advertisement_str = request.POST.get("advertisement_name", "").strip()

    datetime_from = timezone.make_aware(datetime.strptime(date_from_str, "%Y-%m-%d"))
    end_date = timezone.make_aware(datetime.strptime(date_to_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999))

    range_date = (datetime_from, end_date)

    total_count = DXVLLogs.objects.filter(
        advertisement__icontains=advertisement_str,
        date_aired__range=range_date,
    )

    if total_count.count() == 0:
        return "no_logs_found"

    grouped_by_date = (
        DXVLLogs.objects.filter(
            date_aired__range=range_date, advertisement__icontains=advertisement_str
        )
        .annotate(grouped_date=TruncDate("date_aired"))
        .values("grouped_date", "advertisement", "remarks")
        .annotate(no_played=Count("log_id"))
        .order_by("grouped_date")
    )

    monthly_data_logs = []

    for grouped_data in grouped_by_date:

        individual_logs_per_group = (
            DXVLLogs.objects.filter(
                date_aired__date=grouped_data["grouped_date"],
                advertisement__icontains=grouped_data["advertisement"],
                remarks=grouped_data["remarks"],
            ).annotate(
                time=TruncTime('date_aired'),
            )
        )

        time_data = {f"time{i}": individual_log.time.strftime('%I:%M %p') for i, individual_log in enumerate(individual_logs_per_group)}

        monthly_data_logs.append({
                "grouped_data": grouped_data["grouped_date"].strftime("%Y-%m-%d"),
                "advertisement": grouped_data["advertisement"],
                "spots": time_data,
                "remarks": grouped_data["remarks"],
        })

    max_spots = 0
    for log in monthly_data_logs:
        num_spots = len(log['spots'])
        if num_spots > max_spots:
            max_spots = num_spots

    context["monthly_logs"] = monthly_data_logs
    context["max_spots"] = max_spots
    context["total_ads"] = total_count.count()
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

def export_daily_report(request):
    context = {}

    date_from_str = request.POST.get("date_from")
    advertisement_str = request.POST.get("advertisement_name", "").strip()

    datetime_from = timezone.make_aware(datetime.strptime(date_from_str, "%Y-%m-%d"))

    total_count = DXVLLogs.objects.filter(
        advertisement__icontains=advertisement_str,
        date_aired__date=datetime_from,
    )

    if total_count.count() == 0:
        return "no_logs_found"

    grouped_by_date = (
        DXVLLogs.objects.filter(
            date_aired__date=datetime_from, advertisement__icontains=advertisement_str
        )
        .annotate(grouped_date=TruncDate("date_aired"))
        .values("grouped_date", "advertisement", "remarks")
        .annotate(no_played=Count("log_id"))
        .order_by("grouped_date")
    )

    monthly_data_logs = []

    for grouped_data in grouped_by_date:

        individual_logs_per_group = (
            DXVLLogs.objects.filter(
                date_aired__date=grouped_data["grouped_date"],
                advertisement__icontains=grouped_data["advertisement"],
                remarks=grouped_data["remarks"],
            ).annotate(
                time=TruncTime('date_aired'),
            )
        )

        time_data = {f"time{i}": individual_log.time.strftime('%I:%M %p') for i, individual_log in enumerate(individual_logs_per_group)}

        monthly_data_logs.append({
                "grouped_data": grouped_data["grouped_date"].strftime("%Y-%m-%d"),
                "advertisement": grouped_data["advertisement"],
                "spots": time_data,
                "remarks": grouped_data["remarks"],
        })

    max_spots = 0
    for log in monthly_data_logs:
        num_spots = len(log['spots'])
        if num_spots > max_spots:
            max_spots = num_spots

    context["monthly_logs"] = monthly_data_logs
    context["max_spots"] = max_spots
    context["total_ads"] = total_count.count()
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/template_monthly.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"daily_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename

def generate_weekly_report(request):
    context = {}

    date_from_str = request.POST.get("date_from")
    date_to_str = request.POST.get("date_to")
    advertisement_str = request.POST.get("advertisement_name", "").strip()

    datetime_from = timezone.make_aware(datetime.strptime(date_from_str, "%Y-%m-%d"))
    datetime_to = datetime.strptime(date_to_str, "%Y-%m-%d")
    
    end_date = timezone.make_aware(datetime_to.replace(hour=23, minute=59, second=59, microsecond=999999))

    range_date = (datetime_from, end_date)

    total_count = DXVLLogs.objects.filter(
        advertisement__icontains=advertisement_str,
        date_aired__range=range_date,
    )

    if total_count.count() == 0:
        return "no_logs_found"

    grouped_by_date = (
        DXVLLogs.objects.filter(
            date_aired__range=range_date, advertisement__icontains=advertisement_str
        )
        .annotate(grouped_date=TruncDate("date_aired"))
        .values("grouped_date", "advertisement", "remarks")
        .annotate(no_played=Count("log_id"))
        .order_by("grouped_date")
    )

    monthly_data_logs = []

    for grouped_data in grouped_by_date:

        individual_logs_per_group = (
            DXVLLogs.objects.filter(
                date_aired__date=grouped_data["grouped_date"],
                advertisement__icontains=grouped_data["advertisement"],
                remarks=grouped_data["remarks"],
            ).annotate(
                time=TruncTime('date_aired'),
            )
        )

        time_data = {f"time{i}": individual_log.time.strftime('%I:%M %p') for i, individual_log in enumerate(individual_logs_per_group)}

        monthly_data_logs.append({
                "grouped_data": grouped_data["grouped_date"].strftime("%Y-%m-%d"),
                "advertisement": grouped_data["advertisement"],
                "spots": time_data,
                "remarks": grouped_data["remarks"],
        })

    max_spots = 0
    for log in monthly_data_logs:
        num_spots = len(log['spots'])
        if num_spots > max_spots:
            max_spots = num_spots

    context["monthly_logs"] = monthly_data_logs
    context["max_spots"] = max_spots
    context["total_ads"] = total_count.count()
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/template_monthly.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"weekly_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename

def generate_daily_testing_report(request):
    context = {}

    date_from_str = request.POST.get("date_from")
    advertisement_str = request.POST.get("advertisement_name", "").strip()
    date_from = timezone.make_aware(datetime.strptime(date_from_str, "%Y-%m-%d"))

    total_count = DXVLLogs.objects.filter(
        advertisement__icontains=advertisement_str,
        date_aired__date=date_from_str,
    )

    if total_count.count() == 0:
        return "no_logs_found"

    grouped_by_date = (
        DXVLLogs.objects.filter(
            date_aired__date=date_from, advertisement__icontains=advertisement_str
        )
        .annotate(grouped_date=TruncDate("date_aired"))
        .values("grouped_date", "advertisement", "remarks")
        .annotate(no_played=Count("log_id"))
        .order_by("grouped_date")
    )

    monthly_data_logs = []

    for grouped_data in grouped_by_date:

        individual_logs_per_group = (
            DXVLLogs.objects.filter(
                date_aired__date=grouped_data["grouped_date"],
                advertisement__icontains=grouped_data["advertisement"],
                remarks=grouped_data["remarks"],
            ).annotate(
                time=TruncTime('date_aired'),
            )
        )

        time_data = {f"time{i}": individual_log.time.strftime('%I:%M %p') for i, individual_log in enumerate(individual_logs_per_group)}

        monthly_data_logs.append({
                "grouped_data": grouped_data["grouped_date"].strftime("%Y-%m-%d"),
                "advertisement": grouped_data["advertisement"],
                "spots": time_data,
                "remarks": grouped_data["remarks"],
        })

    max_spots = 0
    for log in monthly_data_logs:
        num_spots = len(log['spots'])
        if num_spots > max_spots:
            max_spots = num_spots

    context["monthly_logs"] = monthly_data_logs
    context["max_spots"] = max_spots
    context["total_ads"] = total_count.count()
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/template_monthly.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"daily_daily_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename

def generate_by_company_report(request, keyword, from_date, to_date):
    context = {}


    if from_date and to_date:

        date_from = timezone.make_aware(datetime.strptime(from_date, "%Y-%m-%d"))
        date_to = timezone.make_aware(datetime.strptime(to_date, "%Y-%m-%d"))
        end_date = date_to.replace(hour=23, minute=59, second=59, microsecond=999999)

        total_count = DXVLLogs.objects.filter(
            advertisement__icontains=keyword,
            date_aired__range=(date_from, end_date),
        )


        grouped_by_date = (
            DXVLLogs.objects.filter(
                advertisement__icontains=keyword,
                date_aired__range=(date_from, end_date)
            )
            .annotate(grouped_date=TruncDate("date_aired"))
            .values("grouped_date", "advertisement", "remarks")
            .annotate(no_played=Count("log_id"))
            .order_by("grouped_date")
        )
        
    else:
        total_count = DXVLLogs.objects.filter(
            advertisement__icontains=keyword,
        )

        grouped_by_date = (
            DXVLLogs.objects.filter(
                advertisement__icontains=keyword,
            )
            .annotate(grouped_date=TruncDate("date_aired"))
            .values("grouped_date", "advertisement", "remarks")
            .annotate(no_played=Count("log_id"))
            .order_by("grouped_date")
        )

    if total_count.count() == 0:
        return "no_logs_found"


    monthly_data_logs = []

    for grouped_data in grouped_by_date:

        individual_logs_per_group = (
            DXVLLogs.objects.filter(
                date_aired__date=grouped_data["grouped_date"],
                advertisement__icontains=grouped_data["advertisement"],
                remarks=grouped_data["remarks"],
            ).annotate(
                time=TruncTime('date_aired'),
            )
        )

        time_data = {f"time{i}": individual_log.time.strftime('%I:%M %p') for i, individual_log in enumerate(individual_logs_per_group)}

        monthly_data_logs.append({
                "grouped_data": grouped_data["grouped_date"].strftime("%Y-%m-%d"),
                "advertisement": grouped_data["advertisement"],
                "spots": time_data,
                "remarks": grouped_data["remarks"],
        })

    max_spots = 0
    for log in monthly_data_logs:
        num_spots = len(log['spots'])
        if num_spots > max_spots:
            max_spots = num_spots

    context["company_advertisement"] = monthly_data_logs
    context["max_spots"] = max_spots
    context["total_ads"] = total_count.count()
    context["generated_date"] = datetime.now().strftime("%Y-%m-%d")
    html_string = render_to_string("pdf_template/overall_advertisement.html", context)
    pdf_file = BytesIO()

    try:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            pdf_file
        )
    except Exception:
        return "unexpected_error"

    filename = f"{keyword}_report-{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf_dir = os.path.join(MEDIA_ROOT, "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, filename)

    with open(pdf_path, "wb") as pdf_file_out:
        pdf_file_out.write(pdf_file.getvalue())

    return filename
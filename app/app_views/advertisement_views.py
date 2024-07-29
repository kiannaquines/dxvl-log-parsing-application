import os
from django.shortcuts import render
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from app.commons.logs_services import *
from django.urls import reverse_lazy
from app.models import DXVLLogs
from django.contrib.auth.decorators import login_required
from app.commons.common_services import (
    all_objects_only,
    all_objects_only_with_order,
    pagination,
)
from app.commons.tasks import (
    generate_monthly_report,
    generate_weekly_report,
    generate_daily_report,
)
from django.contrib import messages
from datetime import datetime
from dxvl.settings import BASE_DIR
from django.http import HttpResponseRedirect, FileResponse, HttpResponse
from django.urls import reverse_lazy
from django.db.models import F, Count, Value, CharField, Case, When
from django.db.models.functions import (
    ExtractDay,
    ExtractYear,
    TruncMonth,
    ExtractMonth,
    Concat,
)


@login_required(login_url=reverse_lazy("login"))
def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES.items()
        result = parse_dxvl_logs(user=request.user.username, log_files=files)

        if result == "file_exists":

            return JsonResponse(
                {
                    "type": result,
                    "message": "Logs with the same name already exist or already process by the system.",
                }
            )

        elif result == "file_error":

            return JsonResponse(
                {
                    "type": result,
                    "message": "Your logs seems to have a problem or malformed. Please check and try again.",
                }
            )

        elif result == "success":
            return JsonResponse(
                {
                    "type": result,
                    "message": "Your logs have been successfully parsed. Please check the logs entry for results.",
                }
            )

        else:

            return JsonResponse(
                {
                    "message": "An error occurred while parsing your logs. Please try again later."
                }
            )

    return JsonResponse(
        {
            "message": "An error occurred while processing your request. Please try again later."
        }
    )


@login_required(login_url=reverse_lazy("login"))
def upload_advertisement_logs(request):
    return render(request, "upload.html")


@login_required(login_url=reverse_lazy("login"))
def advertisement_pricing(request):
    return render(request, "pricing.html")


@login_required(login_url=reverse_lazy("login"))
def dxvl_logs_view(request):
    context = {}
    dxvl_logs = all_objects_only_with_order(
        DXVLLogs.objects,
        "date_aired",
        "artist",
        "advertisement",
        "status",
        "date_added",
    )
    page_obj = pagination(dxvl_logs, request.GET.get("page"), 50)
    context["page_object"] = page_obj
    return render(request, "dxvl_logs.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_daily_report_view(request):
    context = {}
    dxvl_logs = all_objects_only(
        DXVLLogs.objects,
        "date_aired",
        "artist",
        "advertisement",
        "status",
        "date_added",
    ).order_by("-date_aired")
    page_obj = pagination(dxvl_logs, request.GET.get("page"), 50)
    context["page_object"] = page_obj
    return render(request, "daily.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_weekly_report_view(request):
    context = {}
    dxvl_logs = all_objects_only(
        DXVLLogs.objects,
        "date_aired",
        "artist",
        "advertisement",
        "status",
        "date_added",
    ).order_by("-date_aired")

    page_obj = pagination(dxvl_logs, request.GET.get("page"), 50)
    context["page_object"] = page_obj
    return render(request, "weekly.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_monthly_report_view(request):
    context = {}
    grouped_ads = (
        DXVLLogs.objects.values("advertisement")
        .annotate(ads_count=Count("log_id"))
        .values("ads_count", "advertisement")
        .order_by("-ads_count")
    )

    grouped_logs = (
        DXVLLogs.objects.annotate(trunc_month=TruncMonth("date_aired"))
        .annotate(
            month=ExtractMonth("trunc_month"),
            day=ExtractDay("trunc_month"),
            year=ExtractYear("trunc_month"),
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
            full_date=Concat(
                F("month_padded"),
                Value("/"),
                F("day_padded"),
                Value("/"),
                F("year"),
                output_field=CharField(),
            ),
        )
        .values("advertisement", "full_date", "artist", "status", "remarks")
        .annotate(ads_count=Count("log_id"))
        .order_by("advertisement")
    )

    page_obj = pagination(grouped_logs, request.GET.get("page"), 100)
    context["page_object"] = page_obj
    context["grouped_ads"] = grouped_ads
    return render(request, "monthly.html", context)


@login_required(login_url=reverse_lazy("login"))
def daily_view(request):
    if request.method == "POST":

        response = HttpResponse(content_type="application/pdf")

        response["Content-Disposition"] = (
            f'attachment; filename="dxvl_daily_report-{datetime.now()}.pdf"'
        )

        result = generate_daily_report(
            date=request.POST.get("daily"),
            response=response,
        )

        if result == "no_logs_found":

            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="warning",
            )

            return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))

        elif result == "error_in_parsing_pdf":

            messages.error(
                request,
                "An error occurred while generating the PDF report. Please try again later.",
                extra_tags="danger",
            )

            return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))

        else:

            return response

    messages.error(
        request,
        "Invalid request method. Only POST requests are allowed.",
        extra_tags="danger",
    )

    return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))


@login_required(login_url=reverse_lazy("login"))
def weekly_view(request):
    if request.method == "POST":
        week_data = request.POST.get("week_from")
        result = generate_weekly_report(request=request, week=week_data)

        if result == "no_logs_found":
            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="warning",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_weekly_report_view"))

        elif result == "error_in_parsing_pdf":
            messages.error(
                request,
                "An error occurred while generating the PDF report. Please try again later.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_weekly_report_view"))

        else:
            pdf_path = os.path.join(BASE_DIR, "media", "pdfs", result)
            if os.path.exists(pdf_path):
                response = FileResponse(
                    open(pdf_path, "rb"), content_type="application/pdf"
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="{os.path.basename(pdf_path)}"'
                )
                return response
            else:
                messages.error(
                    request,
                    "The generated file could not be found.",
                    extra_tags="danger",
                )
                return HttpResponseRedirect(reverse_lazy("dxvl_weekly_report_view"))

    messages.error(
        request,
        "Invalid request method. Only POST requests are allowed.",
        extra_tags="danger",
    )
    return HttpResponseRedirect(reverse_lazy("dxvl_weekly_report_view"))


@login_required(login_url=reverse_lazy("login"))
def monthly_view(request):
    if request.method == "POST":
        result = generate_monthly_report(request=request)
        print(result)


    return HttpResponseBadRequest(
        "Invalid request method. Only POST requests are allowed."
    )

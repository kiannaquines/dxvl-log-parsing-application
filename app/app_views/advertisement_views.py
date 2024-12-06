import os
from django.shortcuts import render
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from app.commons.logs_services import *
from django.urls import reverse_lazy
from app.models import DXVLLogs,Advertisements
from django.contrib.auth.decorators import login_required
from app.commons.common_services import (
    all_objects_only,
    all_objects_only_with_order,
    pagination,
)
from app.commons.generate_report_services import (
    export_daily_report,
    generate_daily_testing_report,
    generate_monthly_report,
    generate_weekly_overall_report,
    generate_weekly_report,
    generate_daily_report,
)
from django.contrib import messages
from app.forms import UpdateAdvertismentInfoForm
from dxvl.settings import BASE_DIR
from django.http import HttpResponseRedirect, FileResponse
from django.db.models import Count
from django.db.models.functions import (
    TruncDate,
)
from django.db.models.functions import Lower
from django.db import IntegrityError
from django.views.generic import UpdateView

class UpdateAdvertismentInfoView(UpdateView):
    pk_url_kwarg = "pk"
    model = Advertisements
    form_class = UpdateAdvertismentInfoForm
    success_url = reverse_lazy("advertisements")
    template_name = "form_templates/edit_advertisement.html"

    def form_valid(self, form):
        messages.error(self.request, "You have successfully updated the price of advertisement.",extra_tags="primary")
        response = super().form_valid(form)
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error updating advertisement information.", extra_tags="danger")
        return super().form_invalid(form)

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
def advertisements(request):
    context = {}

    if request.method == "POST":
        price = request.POST.get("ad_price")
        advertisement_name = request.POST.get("advertisement_name","").strip()

        try:

            Advertisements.objects.create(
                advertisement_price=price,
                advertisement_name=advertisement_name,
            )

            messages.error(request, "Advertisement have successfully added new advertisement.",extra_tags="primary")
            return HttpResponseRedirect(reverse_lazy("advertisements"))
        
        except IntegrityError:
            messages.error(request, "Advertisement already exists.",extra_tags="danger")
            return HttpResponseRedirect(reverse_lazy("advertisements"))

    grouped_ads = (
        DXVLLogs.objects.values(lowered_adname=Lower("advertisement"))
        .annotate(ads_count=Count("log_id"))
        .values("ads_count","advertisement","lowered_adname")
        .order_by("-ads_count")
    )

    dxvl_logs = Advertisements.objects.all().order_by("-date_added")[:50]

    page_obj = pagination(dxvl_logs, request.GET.get("page"), 50)
    
    context["page_object"] = page_obj
    context['grouped_ads'] = grouped_ads
    return render(request, "advertisement.html",context)


def delete_advertisement(request, pk):
    try:
        Advertisements.objects.filter(advertisement_id=pk).delete()
        messages.success(request, "Advertisement has been successfully deleted.", extra_tags="primary")
    except Exception as e:
        messages.error(request, f"Error deleting advertisement: {str(e)}", extra_tags="danger")
    
    return HttpResponseRedirect(reverse_lazy("advertisements"))


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
    page_obj = pagination(dxvl_logs, request.GET.get("page"), 2000)
    context["page_object"] = page_obj
    return render(request, "dxvl_logs.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_daily_report_view(request):
    context = {}
    advertisements = Advertisements.objects.all().order_by("-date_added")
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
    context["ads"] = advertisements
    return render(request, "daily.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_weekly_report_view(request):
    context = {}
    advertisements = Advertisements.objects.all().order_by("-date_added")
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
    context["ads"] = advertisements
    return render(request, "weekly.html", context)


@login_required(login_url=reverse_lazy("login"))
def dxvl_monthly_report_view(request):
    context = {}
    advertisements = Advertisements.objects.all().order_by("-date_added")

    grouped_logs = (
        DXVLLogs.objects.annotate(date=TruncDate("date_aired"))
        .values("advertisement", "date", "artist", "status", "remarks")
        .annotate(ads_count=Count("log_id"))
        .order_by("-ads_count")
    )

    page_obj = pagination(grouped_logs, request.GET.get("page"), 100)
    context["page_object"] = page_obj
    context["ads"] = advertisements
    return render(request, "monthly.html", context)


@login_required(login_url=reverse_lazy("login"))
def daily_view(request):
    if request.method == "POST":


        result = generate_daily_report(
            date=request.POST.get("daily"),
            request=request,
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
                return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))

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
        result = generate_weekly_overall_report(request=request, week=week_data)

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
    
        if result == "no_logs_found":
            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_monthly_report_view"))
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

    return HttpResponseBadRequest(
        "Invalid request method. Only POST requests are allowed."
    )


@login_required(login_url=reverse_lazy("login"))
def daily_export_view(request):
    if request.method == "POST":
        print(request.POST)
        result = generate_daily_report(request=request)
    
        if result == "no_logs_found":
            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_monthly_report_view"))
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

    return HttpResponseBadRequest(
        "Invalid request method. Only POST requests are allowed."
    )


@login_required(login_url=reverse_lazy("login"))
def weekly_export_view(request):
    if request.method == "POST":
        result = generate_weekly_report(request=request)
    
        if result == "no_logs_found":
            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_monthly_report_view"))
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

    return HttpResponseBadRequest(
        "Invalid request method. Only POST requests are allowed."
    )

@login_required(login_url=reverse_lazy("login"))
def daily_testing_export_view(request):
    if request.method == "POST":
        result = generate_daily_testing_report(request=request)
    
        if result == "no_logs_found":
            messages.info(
                request,
                "Sorry, no logs found from the given date.",
                extra_tags="danger",
            )
            return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))
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
                return HttpResponseRedirect(reverse_lazy("dxvl_daily_report_view"))

    return HttpResponseBadRequest(
        "Invalid request method. Only POST requests are allowed."
    )

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.commons.logs_services import *
from app.commons.common_services import all_objects_only,all_objects_only_with_order,pagination
from django.urls import reverse_lazy
from app.models import DXVLLogs
from django.http import HttpResponseBadRequest
from app.commons.generate_report_services import generate_monthly_report, generate_weekly_report, generate_daily_report

@login_required(login_url=reverse_lazy('login'))
def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES.items()
        result = parse_dxvl_logs(user=request.user.username,log_files=files)

        if result == 'file_exists':

            return JsonResponse({
                    "type": result,
                    "message": "Logs with the same name already exist or already process by the system."
            })
        
        elif result == 'file_error':

            return JsonResponse({
                "type": result,
                "message": "Your logs seems to have a problem or malformed. Please check and try again."
            })
        
        elif result == 'success':
            return JsonResponse({
                "type": result,
                "message": "Your logs have been successfully parsed. Please check the logs entry for results."
            })
        
        else:

            return JsonResponse({
                "message": "An error occurred while parsing your logs. Please try again later."
            })
        
    return JsonResponse({
        "message": "An error occurred while processing your request. Please try again later."
    })
        
@login_required(login_url=reverse_lazy('login'))
def upload_advertisement_logs(request):
    return render(request,"upload.html")

@login_required(login_url=reverse_lazy('login'))
def advertisement_pricing(request):
    return render(request,"pricing.html")

@login_required(login_url=reverse_lazy('login'))
def dxvl_logs_view(request):
    context   = {}
    dxvl_logs = all_objects_only_with_order(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    page_obj  = pagination(dxvl_logs,request.GET.get('page'),50)
    context['page_object'] = page_obj
    return render(request, 'dxvl_logs.html',context)


@login_required(login_url=reverse_lazy('login'))
def dxvl_daily_report_view(request):
    context   = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    page_obj  = pagination(dxvl_logs,request.GET.get('page'),50)
    context['page_object'] = page_obj
    return render(request, 'daily.html',context)

@login_required(login_url=reverse_lazy('login'))
def dxvl_weekly_report_view(request):
    context   = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    page_obj  = pagination(dxvl_logs,request.GET.get('page'),50)
    context['page_object'] = page_obj
    return render(request, 'weekly.html',context)

@login_required(login_url=reverse_lazy('login'))
def dxvl_monthly_report_view(request):
    context   = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    page_obj  = pagination(dxvl_logs,request.GET.get('page'),50)
    context['page_object'] = page_obj
    return render(request, 'monthly.html',context)

@login_required(login_url=reverse_lazy('login'))
def daily_view(request):
    if request.method == "POST":
        result = generate_daily_report(start_date=request.POST.get('date_from'), end_date=request.POST.get('date_to'))

    return HttpResponseBadRequest("Invalid request method. Only POST requests are allowed.")

@login_required(login_url=reverse_lazy('login'))
def weekly_view(request):
    if request.method == "POST":
        pass

    return HttpResponseBadRequest("Invalid request method. Only POST requests are allowed.")

@login_required(login_url=reverse_lazy('login'))
def monthly_view(request):
    if request.method == "POST":
        pass

    return HttpResponseBadRequest("Invalid request method. Only POST requests are allowed.")

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from app.commons.logs_services import *
from app.commons.common_services import all_objects_only
from django.urls import reverse_lazy
from app.models import DXVLLogs
from django.core.paginator import Paginator

@login_required(login_url=reverse_lazy('login'))
def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES.items()
        result = parse_dxvl_logs(files)

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

def advertisement_pricing(request):
    return render(request,"pricing.html")

def dxvl_logs_view(request):
    context = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    paginator = Paginator(dxvl_logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_object'] = page_obj
    return render(request, 'dxvl_logs.html',context)

def dxvl_monthly_report_view(request):
    context = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    paginator = Paginator(dxvl_logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_object'] = page_obj
    return render(request, 'monthly.html',context)


def dxvl_daily_report_view(request):
    context = {}
    dxvl_logs = all_objects_only(DXVLLogs.objects,'date_aired','artist','advertisement','status','date_added')
    paginator = Paginator(dxvl_logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_object'] = page_obj
    return render(request, 'daily.html',context)
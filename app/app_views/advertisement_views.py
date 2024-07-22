from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
from app.commons.logs_services import *
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('login'))
def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES.items()
        result = parse_dxvl_logs(files)

        if result == 'file_exists':
            
            return JsonResponse({
                    "type": result,
                    "message": "Logs with the same name already exist. Please rename your logs and try again."
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
    return render(request, 'dxvl_logs.html')
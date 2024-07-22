from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from app.commons.logs_services import *
from django.urls import reverse_lazy

@login_required(login_url=reverse_lazy('login'))
def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES.items()
        parse_dxvl_logs(request, files)
    return HttpResponse("File uploaded successfully")

@login_required(login_url=reverse_lazy('login'))
def upload_advertisement_logs(request):
    return render(request,"upload.html")

def advertisement_pricing(request):
    return render(request,"pricing.html")

def dxvl_logs_view(request):
    return render(request, 'dxvl_logs.html')
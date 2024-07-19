from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.commons.services import *
from django.http import HttpResponse

def upload_advertisement_logs(request):
    return render(request,"upload.html")

def advertisement_pricing(request):
    return render(request,"pricing.html")

def users_permissions(request):
    return render(request,"user_permission.html")

def users_group(request):
    return render(request,"user_groups.html")

def users(request):
    return render(request,"users.html")

def login_page_view(request):
    return render(request, 'login.html')

def register_page_view(request):
    return render(request, 'register.html')

def dashboard_page_view(request):
    return render(request, 'dashboard.html')

def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES
        print(files)
    return HttpResponse("File uploaded successfully")

def dxvl_logs_view(request):
    return render(request, 'dxvl_logs.html')




    

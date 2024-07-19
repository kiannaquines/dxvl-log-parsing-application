from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.commons.services import *
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def dashboard_page_view(request):
    return render(request, 'dashboard.html')

def parse_logs_view(request):
    if request.method == "POST":
        pass

def dxvl_logs_view(request):
    return render(request, 'dxvl_logs.html')




    

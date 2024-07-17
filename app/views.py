from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.commons.services import *

def dashboard_page_view(request):
    return render(request, 'dashboard.html')




    

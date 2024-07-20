from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.forms import *
from app.commons.common_services import *
from django.http import HttpResponse


def login_page_view(request):
    return render(request, 'login.html')

def register_page_view(request):
    return render(request, 'register.html')





    

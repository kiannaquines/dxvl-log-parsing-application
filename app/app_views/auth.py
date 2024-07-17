from django.shortcuts import render
from app.forms import *
from app.commons.services import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_page_view(request):
    return render(request, 'login.html')

def register_page_view(request):
    return render(request, 'register.html')
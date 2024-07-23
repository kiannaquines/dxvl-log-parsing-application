from django.shortcuts import render
from app.decorators import already_loggedin
from app.forms import *
from app.commons.common_services import *
from django.http import HttpResponse

@already_loggedin
def login_page_view(request):
    return render(request, 'login.html')

@already_loggedin
def register_page_view(request):
    return render(request, 'register.html')





    

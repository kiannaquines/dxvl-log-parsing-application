from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def login_page(req):
    return render(req, 'login.html')
    

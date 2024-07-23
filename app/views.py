from django.shortcuts import render
from app.decorators import already_loggedin
from app.forms import *
from app.commons.common_services import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from app.forms import RegisterUserForm,LoginForm

@already_loggedin
def login_page_view(request):
    context = {}
    form = LoginForm()
    if request.method == 'POST':
        pass
    context['login_form'] = form
    return render(request, 'login.html',context)

@already_loggedin
def register_page_view(request):
    context = {}
    form = RegisterUserForm(request.POST)
    if request.method == 'POST':
        pass
    context['register_form'] = form
    return render(request, 'register.html',context)

def signout(request):
    logout(request)
    return redirect(reverse_lazy('login'))
    

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
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('dashboard'))
            else:
                context['error'] = 'Invalid username or password, please try again.'

    context['login_form'] = form
    return render(request, 'login.html',context)

@already_loggedin
def register_page_view(request):
    context = {}
    form = RegisterUserForm()
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            return redirect(reverse_lazy('login'))
        else:
            context['error'] = 'Please check your input, registration failed try again.'

    context['register_form'] = form
    return render(request, 'register.html',context)

def signout(request):
    logout(request)
    return redirect(reverse_lazy('login'))
    

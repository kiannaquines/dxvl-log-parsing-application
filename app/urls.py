from django.urls import path
from app.views import *

urlpatterns = [
    path('',login_page,name="login"),
]
from django.urls import path
from app.views import *
from app.app_views.auth import *
from app.views import dashboard_page_view

urlpatterns = [
    path('',login_page_view,name="login"),
    path('register/',register_page_view,name="register"),
    path('dashboard/',dashboard_page_view,name="dashboard"),
]
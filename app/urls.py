from django.urls import path
from app.views import login_page_view,register_page_view,dashboard_page_view, dxvl_logs_view

urlpatterns = [
    path('',login_page_view,name="login"),
    path('register/',register_page_view,name="register"),
    path('dashboard/',dashboard_page_view,name="dashboard"),
    path('aired/',dxvl_logs_view,name="dxvl_logs_view"),
]
from django.urls import path
from app.views import *

urlpatterns = [
    path('',login_page_view,name="login"),
    path('register/',register_page_view,name="register"),
    path('dashboard/',dashboard_page_view,name="dashboard"),
    path('aired/',dxvl_logs_view,name="logs_view"),

    path('users/',users,name="users"),
    path('users/groups',users_group,name="users_group"),
    path('users/permission',users_permissions,name="users_permission"),
]
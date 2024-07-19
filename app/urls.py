from django.urls import path
from app.views import *

urlpatterns = [

    # Auth routes
    path('',login_page_view,name="login"),
    path('register/',register_page_view,name="register"),

    # Dashboard routes
    path('dashboard/',dashboard_page_view,name="dashboard"),
    path('dashboard/advertisement/logs',dxvl_logs_view,name="logs_view"),
    path('dashboard/advertisement/logs/uploads',upload_advertisement_logs,name="upload_advertisement_logs"),
    path('dashboard/advertisement/pricing',advertisement_pricing,name="advertisement_pricing"),

    # User routes
    path('dashbboard/users/',users,name="users"),
    path('dashboard/users/groups',users_group,name="users_group"),
    path('dashboard/users/permission',users_permissions,name="users_permission"),

    # Parse logs routes
    path('dashboard/advertisement/logs/uploads/upload',parse_logs_view,name="parse_logs_view"),
]
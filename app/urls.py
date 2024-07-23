from django.urls import path
from app.views import *
from app.app_views.advertisement_views import *
from app.app_views.dashboard_views import *
from app.app_views.users_views import *

urlpatterns = [

    # Auth routes
    path('',login_page_view,name="login"),
    path('register/',register_page_view,name="register"),
    path('user/signout',signout,name="signout"),

    # Dashboard routes
    path('dashboard/',dashboard_page_view,name="dashboard"),
    path('dashboard/advertisement/logs',dxvl_logs_view,name="logs_view"),
    path('dashboard/advertisement/logs/uploads',upload_advertisement_logs,name="upload_advertisement_logs"),
    path('dashboard/advertisement/pricing',advertisement_pricing,name="advertisement_pricing"),
    path('dashboard/advertisement/report/daily',dxvl_daily_report_view,name="dxvl_daily_report_view"),
    path('dashboard/advertisement/report/weekly',dxvl_weekly_report_view,name="dxvl_weekly_report_view"),
    path('dashboard/advertisement/report/monthly',dxvl_monthly_report_view,name="dxvl_monthly_report_view"),

    # Generate Reports routes

    
    # User routes
    path('dashbboard/users/',users,name="users"),
    path('dashboard/users/new/',NewUserView.as_view(),name="new_user"),
    path('dashboard/users/<int:pk>/edit/',EditUserView.as_view(),name="edit_user"),
    path('dashboard/users/<int:pk>/delete/',DeleteUserView.as_view(),name="delete_user"),
    
    # Parse logs routes
    path('dashboard/advertisement/logs/uploads/upload',parse_logs_view,name="parse_logs_view"),
]
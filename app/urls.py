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
    path('dashboard/advertisement/daily/logs',fetch_current_year_daily_logs,name="fetch_daily_logs"),
    path('dashboard/advertisement',advertisements,name="advertisements"),
    path('dashboard/advertisement/report/daily',dxvl_daily_report_view,name="dxvl_daily_report_view"),
    path('dashboard/advertisement/report/weekly',dxvl_weekly_report_view,name="dxvl_weekly_report_view"),
    path('dashboard/advertisement/report/monthly',dxvl_monthly_report_view,name="dxvl_monthly_report_view"),
    path('dashboard/advertisement/delete/<int:pk>',delete_advertisement,name="delete_advertisement"),

    # Generate Reports routes General Report routes
    path('dashboard/advertisement/report/daily/generate',daily_view,name="daily_report_generate"),
    path('dashboard/advertisement/report/weekly/generate',weekly_view,name="weekly_report_generate"),
    path('dashboard/advertisement/report/monthly/generate',monthly_view,name="monthly_report_generate"),


    # Export PDF for Daily, Weekly, and Monthly Reports
    path('dashboard/advertisement/report/daily/export',daily_testing_export_view,name="daily_testing_export_view"),
    path('dashboard/advertisement/report/weekly/export',weekly_export_view,name="weekly_export_view"),
    
    # User routes
    path('dashbboard/users/',users,name="users"),
    path('dashboard/users/new/',NewUserView.as_view(),name="new_user"),
    path('dashboard/users/<int:pk>/edit/',EditUserView.as_view(),name="edit_user"),
    path('dashboard/users/<int:pk>/delete/',DeleteUserView.as_view(),name="delete_user"),
    
    # Parse logs routes
    path('dashboard/advertisement/logs/uploads/upload',parse_logs_view,name="parse_logs_view"),
    path('generate/billing/',generate_billing_statement,name="generate_billing_statement"),
    path("advertisement/update/<int:pk>", UpdateAdvertismentInfoView.as_view(), name="update_advertisement"),


    # Search Keywords

    path('advertisment/search-keywords/', SearchKeywordsView.as_view(), name="search_keywords"),
    path('advertisment/search-keywords/add', AddSearchKeywordsView.as_view(), name="add_search_keywords"),
    path('advertisment/search-keywords/edit/<int:pk>', UpdateSearchKeywordView.as_view(), name="update_search_keywords"),
    path('advertisment/search-keywords/delete/<int:pk>', DeleteSearchKeywordView.as_view(), name="delete_search_keywords"),

    path('advertisement/search-keywords/export', ExportSearchKeywordView.as_view(), name="export_search_keywords"),
]
from django.shortcuts import render

def dashboard_page_view(request):
    return render(request, 'dashboard.html')
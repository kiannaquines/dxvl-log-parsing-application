from django.shortcuts import render
from app.models import DXVLLogs
from app.commons.common_services import all_objects_only_number

def dashboard_page_view(request):
    context = {}
    dxvl_logs = all_objects_only_number(DXVLLogs.objects, 'date_aired', 'artist', 'advertisement','status',number=30)
    context['dxvl_logs'] = dxvl_logs
    return render(request, 'dashboard.html',context)
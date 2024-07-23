from django.shortcuts import render
from app.models import DXVLLogs,DXVLUsers
from app.commons.common_services import all_objects_only_with_order_limit,count_objects,filter_objects_count
from app.utils.utilities import get_current_week, get_last_week_time

def dashboard_page_view(request):
    context = {}

    last_week_date = get_last_week_time()
    start_week, end_week = get_current_week()

    #  Total Count
    result_total_logs_this_week = filter_objects_count(DXVLLogs.objects,date_aired__gte=start_week, date_aired__lte=end_week)
    result_logs_last_week = filter_objects_count(DXVLLogs.objects, date_aired__gte=last_week_date)
    result_total_logs = count_objects(DXVLLogs.objects)
    result_users = count_objects(DXVLUsers.objects)
    # Logs
    dxvl_logs = all_objects_only_with_order_limit(DXVLLogs.objects, "date_aired", "artist", "advertisement","status",limit=30)

    context["dxvl_logs"] = dxvl_logs
    context["total_logs"] = f"{result_total_logs:,}"
    context["total_last_week_logs"] = f"{result_logs_last_week:,}"
    context["total_logs_this_week"] = f"{result_total_logs_this_week:,}"
    context["total_users"] = f"{result_users:,}"

    return render(request, "dashboard.html",context)
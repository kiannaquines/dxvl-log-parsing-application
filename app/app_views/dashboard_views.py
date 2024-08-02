from django.shortcuts import render
from app.models import DXVLLogs,DXVLUsers
from app.commons.common_services import all_objects_only_with_order_limit,count_objects,filter_objects_count
from app.utils.utilities import get_current_week, get_last_week_time
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime,timedelta
from django.utils import timezone

@login_required(login_url=reverse_lazy('login'))
def dashboard_page_view(request):
    context = {}

    last_week_date = get_last_week_time()
    start_week, end_week = get_current_week()

    aware_start_week = timezone.make_aware(start_week)
    aware_end_week = timezone.make_aware(end_week)

    #  Total Count
    result_total_logs_this_week = filter_objects_count(DXVLLogs.objects,date_aired__gte=aware_start_week, date_aired__lte=aware_end_week)
    result_logs_last_week = filter_objects_count(DXVLLogs.objects, date_aired__gte=last_week_date)
    result_total_logs = count_objects(DXVLLogs.objects)
    result_users = count_objects(DXVLUsers.objects)
    
    # Logs
    dxvl_logs = all_objects_only_with_order_limit(DXVLLogs.objects, "date_aired", "artist", "advertisement","status","date_aired",limit=30)

    context["dxvl_logs"] = dxvl_logs
    context["total_logs"] = f"{result_total_logs:,}"
    context["total_last_week_logs"] = f"{result_logs_last_week:,}"
    context["total_logs_this_week"] = f"{result_total_logs_this_week:,}"
    context["total_users"] = f"{result_users:,}"

    return render(request, "dashboard.html",context)


def fetch_current_year_daily_logs(request):
    if request.method == "GET":
        current_year = datetime.now().year

        current_year_daily_logs = list(
            DXVLLogs.objects.annotate(
                date_only_aired=TruncDate('date_aired')
            ).filter(date_only_aired__year=current_year).values(
                'date_only_aired'
            ).annotate(
                daily_count=Count('log_id')
            ).order_by(
                'date_only_aired'
            )
        )

        daily_logs = [
            {
                'year': current_year,
                'logs': current_year_daily_logs,
            },
        ]

        return JsonResponse(daily_logs,safe=False)
    
    return JsonResponse({'message':'invalid_method'})
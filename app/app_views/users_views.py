from django.shortcuts import render
from app.models import DXVLUsers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from app.commons.common_services import all_objects_only

def users(request):
    context = {}
    users_list = all_objects_only(DXVLUsers.objects,'username','email','first_name','last_name','date_joined')
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['users_obj'] = page_obj
    return render(request,"users.html",context)
from django.shortcuts import render
from app.models import DXVLUsers
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from app.commons.common_services import all_objects_only

def users(request):
    context = {}
    users_list = all_objects_only(DXVLUsers.objects,'username','email','first_name','last_name','date_joined')
    context['users_list'] = users_list
    return render(request,"users.html",context)
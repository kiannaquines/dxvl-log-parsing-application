from django.shortcuts import render

def users_permissions(request):
    return render(request,"user_permission.html")

def users(request):
    return render(request,"users.html")
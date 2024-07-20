from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def upload_advertisement_logs(request):
    return render(request,"upload.html")

def advertisement_pricing(request):
    return render(request,"pricing.html")

def parse_logs_view(request):
    if request.method == "POST":
        files = request.FILES
        print(files)
    return HttpResponse("File uploaded successfully")

def dxvl_logs_view(request):
    return render(request, 'dxvl_logs.html')
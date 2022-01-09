from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout


# Create your views here.

def Home_page(request):
    return render(request,"manager/login.html")
def event_page (request):
    return redirect('manager:show_all_events')
def payment (request):
    return redirect('manager:show_all_pyments')
def volunteer (request):
    return redirect('manager:show_all_volunteer')
def Hotel_page (request):
    return redirect('manager:show_all_hotels')
def logout_view(request):
    logout(request)
    return redirect('manager:login_view')
    



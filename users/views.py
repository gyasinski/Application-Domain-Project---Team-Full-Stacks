from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def render_login_page(request):
    return render(request, 'main.html')


def get_login_data(request):
    login_user = request.POST.get('user_name')
    login_password = request.POST.get('user_password')
    return render(request, 'main.html')

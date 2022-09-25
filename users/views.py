from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse

from users.models import User
from users.backend import UserBackend


# Create your views here.

def render_login_page(request):
    return render(request, 'main.html')


def get_login_data(request):
    login_username = request.POST.get('user_name')
    login_password = request.POST.get('user_password')
    backend_instance = UserBackend
    login_request = backend_instance.authenticate(backend_instance, login_username, login_password)
    return HttpResponse('Complete')

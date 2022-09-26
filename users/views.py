from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

from users.models import User
from users.backend import UserBackend

from django.core.mail import send_mail
import random
import string

from django.contrib.auth import get_user_model




# Create your views here.

def render_login_page(request):
    return render(request, 'main.html')

def render_forgot_password_page(request):
    return render(request, 'forgotPassword.html')

def fp_get_creds(request):
    username = request.POST.get('curr_username')
    email = request.POST.get('curr_email')
    curr_user = verify_user_exists_via_email(username,email)
    if curr_user is None:
        print('User not found!')
    else:
        print('User ' + curr_user.get_username() + ' found!')
        send_mail(
        'FullStacks Accounting Password',
        'Hello ' + curr_user.get_first_name() + '!' + ' This email is intended to help you remember your FullStacks Accounting Software password. If you did not request your password, please ignore this email and contact customer service. Otherwise, please see your current password below for future logins. \n Current Password: ' + curr_user.get_password(),
        'from@example.com',
        [email],
        fail_silently=False,
     )

        return render(request,'resetPassword.html')


def generate_pin():
    length = 4
    chars = string.ascii_lowercase
    pin = ''.join(random.choice(chars) for i in range(length))
    print(pin)
    return pin



def get_login_data(request):
    login_username = request.POST.get('user_name')
    login_password = request.POST.get('user_password')
    backend_instance = UserBackend
    login_request = backend_instance.authenticate(backend_instance, login_username, login_password)
    return HttpResponse('Complete')

def verify_user_exists_via_email(username, email):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(username=username, email=email)
        return user
    except User.DoesNotExist:
        print('User not found!')
        pass


def reset_current_password(request):
    return HttpResponse('Complete')

def verify_password(password):
    if len(password) < 8:
        print('not long enough!')
    if any(char.isdigit() for char in password) == False:
        print('Needs a number!')
    if password[0].isalpha() == False:
        print('First character must be a letter!')
    if any(char.isalpha() for char in password) == False:
        print('Needs a letter!')

    special_characters = "!@#$%^&*()-+?_=,<>/"

    if any(c in special_characters for c in password):
        print('yes!')
    else:
        print('Must contain special characters!')
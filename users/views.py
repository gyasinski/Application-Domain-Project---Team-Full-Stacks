from math import perm
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

from users.models import User
from users.backend import UserBackend

from django.core.mail import send_mail
import random
import string

from django.http import HttpResponseRedirect


from django.contrib.auth import get_user_model

from django.shortcuts import redirect





# Create your views here.

def render_create_page(request):
    return render(request, 'create.html')

def render_setpass_page(request):
    return render(request, 'resetPassword.html')

def render_admin_page(request):
    return render(request, 'adminMenu.html')

def render_viewusers_page(request):
    users = User.objects.all()
    return render(request, 'view_users.html', {'users': users})

def render_edituser_page(request):
    return render(request, 'adminEditUser.html')

def render_accountant_page(request):
    return render(request, 'accountantMenu.html')

def render_manager_page(request):
    return render(request, 'managerMenu.html')

def render_login_page(request):
    return render(request, 'main.html')

def render_forgot_password_page(request):
    return render(request, 'forgotPassword.html')

def fp_get_creds(request):
    username = request.POST.get('curr_username')
    email = request.POST.get('curr_email')
    curr_user = verify_user_exists_via_email(username,email)
    if curr_user is None:
        return None
    else:
        print('User ' + curr_user.get_username() + ' found!')
        send_mail(
        'FullStacks Accounting Password',
        'Hello ' + curr_user.get_first_name() + '!' + ' This email is intended to help you remember your FullStacks Accounting Software password. If you did not request your password, please ignore this email and contact customer service. Otherwise, please see your current password below for future logins. \n Current Password: ' + curr_user.get_password(),
        'fullstacktestemail@gmail.com',
        [email],
        fail_silently=False,
     )
        response = redirect('/users/forgot-password')
        return response


def generate_pin():
    length = 4
    chars = string.ascii_lowercase
    pin = ''.join(random.choice(chars) for i in range(length))
    print(pin)
    return pin



def login_user(request):
    login_username = request.POST.get('user_name')
    login_password = request.POST.get('user_password')
    backend_instance = UserBackend
    current_user = backend_instance.authenticate(backend_instance, login_username, login_password)
    if current_user.has_perm(perm):
        response = redirect('/users/administrator')
        return response
    elif current_user.is_accountant:
        response = redirect('/users/accountant')
        return response
    else:
        response = redirect('/users/manager')
        return response

def logout_user(request):
    request.user = None
    return HttpResponseRedirect('/users')

def verify_user_exists_via_email(username, email):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(username=username, email=email)
        return user
    except User.DoesNotExist:
        print('User not found!')
        pass


def reset_current_password(request):
    pass

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


def submit_request_for_new_account(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    apartment_num = request.POST.get('apartment')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    country = request.POST.get('country')
    dob = request.POST.get('date_of_birth')
    admin_user = request.POST.get('admin_user')


    UserModel = get_user_model()
    req_admin = UserModel.objects.get(username=admin_user)
    if req_admin.has_perm(perm):
        admin_name = req_admin.get_first_name()
        admin_email = req_admin.get_email()

        email_string = "Hello " + admin_name + "!" + "\n Below is the information for a new user request." + "\n Applicant Info: \n First Name: " + first_name + "\n Last Name: " + last_name + "\n Street Address: " + address + "\n Apartment: " + apartment_num + "\n City: " + city + "\n State: " + state + "\n Zip Code: " + zip_code + "\n Country: " + country + "\n Date of Birth: " + dob

        send_mail(
            'New User Request',
            email_string,
            'fullstacktestemail@gmail.com',
            [admin_email],
            fail_silently=False,
        )

        return HttpResponseRedirect('/users')
    else:
        print('User has requested the approval of a Full Stacks Accounting Member without appropriate permissions. Please try again.')

    return HttpResponse('/users!')
    
    
    
    
    

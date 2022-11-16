from math import perm
from django.shortcuts import render
from django.http import HttpResponse

from users.models import RequestedUser, User
from django.contrib.auth import authenticate, login

from django.core.mail import send_mail
import random

from django.http import HttpResponseRedirect


from django.contrib.auth import get_user_model

from django.shortcuts import redirect

#############################
from datetime import datetime, timezone
from django.shortcuts import render
import calendar 
from calendar import HTMLCalendar

from django.contrib import messages

import string
import secrets


from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404

from accounts.models import Account

PASSWORD_EXPIRY_THIRTY_DAYS = 30

# Create your views here.

####################################
# Create New User Page and Methods #
####################################

def render_create_page(request):
    return render(request, 'create.html')

def submit_request_for_new_account(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    email = request.POST.get('email_addr')
    apartment_num = request.POST.get('apartment')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')
    country = request.POST.get('country')
    dob = request.POST.get('date_of_birth')
    admin_user = User.objects.get(role="Administrator")
    try:
        fss = FileSystemStorage()
        profile_image_file = fss.save(request.FILES['p_image'].name, request.FILES['p_image'])
        profile_image_url = fss.url(profile_image_file)
    except:
        profile_image_url = 'None'


    try:
        req_id = generate_request_id()
        requested_user = RequestedUser (
            request_id = req_id,
            req_first_name = first_name,
            req_last_name = last_name,
            req_email = email,
            req_address = address,
            req_apartment_or_suite_num = apartment_num,
            req_city = city,
            req_state = state,
            req_zip_code = zip_code,
            req_country = country,
            req_dob = dob,
            req_profile_image = profile_image_url
        )


        requested_user.save()
    except:
        messages.error(request, 'Error, could not send request at this time, Please try again later.')

    messages.success(request, 'Success! Request sent with Request ID: ' + str(req_id) + '. Please attempt a login after your account is created.')


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

def generate_employee_id():
    employee_id = -2
    retry_count = 0
    retry = True
    employee_id = random.randint(1,1001)

    while(retry):
        try:
            if User.objects.get(employee_id=employee_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return employee_id

    employee_id = -1
    return employee_id

def generate_employee_username(fn_initial,ln):

    current_date = datetime.now()
    current_year = (str(current_date.year)[2:])
    current_month = str(current_date.month)

    new_username = fn_initial + ln + current_month + current_year
    return new_username

####################################
#      Set New Password Page       #
####################################

def render_setpass_page(request):
    return render(request, 'resetPassword.html')

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

####################################
#  Administrator Pages and Methods #
####################################

def render_admin_page(request):
    current_admin = request.user
    return render(request, 'adminMenu.html', {'current_admin': current_admin})

def render_viewusers_page(request):
    users = User.objects.all()
    current_admin = request.user
    return render(request, 'view_users.html', {'users': users, 'current_admin': current_admin})

def toggle_active_status(request, pk):
    user = User.objects.get(employee_id=pk)
    user.activate()
    user.save()
    response = redirect('/users/administrator/view_all_users/')
    return response

def render_edituser_page(request, pk):
    user = User.objects.get(employee_id=pk)
    current_admin = request.user
    return render(request, 'adminEditUser.html', {'user': user, 'current_admin': current_admin})

def edit_user(request, pk):
    user = User.objects.get(employee_id=pk)
    user.first_name = request.GET.get('fname')
    user.last_name = request.GET.get('lname')
    user.email = request.GET.get('email')
    user.set_role(request.GET.get('role'))
    user.save()
    response = redirect('/users/administrator/view_all_users/')
    return response

def render_suspenduser_page(request, pk):
    user = User.objects.get(employee_id=pk)
    current_admin = request.user
    return render(request, 'adminSuspendUser.html', {'user': user, 'current_admin': current_admin})

def suspend_user(request, pk):
    user = User.objects.get(employee_id=pk)
    days = int(request.GET.get('suspenddays'))
    hours = int(request.GET.get('suspendhours'))
    mins = int(request.GET.get('suspendmins'))
    user.suspend(days, hours, mins)
    user.save()
    response = redirect('/users/administrator/view_all_users/')
    return response

def render_emailuser_page(request, pk):
    user = User.objects.get(employee_id=pk)
    current_admin = request.user
    return render(request, 'adminEmailUser.html', {'user': user, 'current_admin': current_admin})

def find_user_from_name(request, username):
    user = User.objects.get(username=username)
    temp_id = user.employee_id
    response = redirect('/users/administrator/email_user/'+str(temp_id)+'/')
    return response

def email_user(request, pk):
    user = User.objects.get(employee_id=pk)

    subject_str = request.GET.get('emailsubject')
    body_str = request.GET.get('emailbody')
    user_email = user.get_email()

    send_mail(
        subject_str,
        body_str,
        'fullstacktestemail@gmail.com',
        [user_email],
        fail_silently=False,
    )

    response = redirect('/users/administrator/view_all_users/')
    return response

def render_unapproved_users_page(request):
    unapproved_users = RequestedUser.objects.all()
    current_admin = request.user
    return render(request, 'unapprovedUsers.html', {'unapproved_users': unapproved_users, 'current_admin':current_admin})

def approved_user(request):
    try:
        request_id = request.POST.get('request_id')
        req_user = RequestedUser.objects.get(request_id=request_id)
        new_employee_id = generate_employee_id()
        employee_first_initial = req_user.req_first_name
        new_employee_username = generate_employee_username(employee_first_initial[0], req_user.req_last_name)
        new_password = generate_random_password()

        new_user = User(
            employee_id=new_employee_id,
            email=req_user.req_email,
            username=new_employee_username,
            first_name=req_user.req_first_name,
            last_name=req_user.req_last_name,
            password=new_password,
            password_date_time=datetime.now(),
            date_of_birth=req_user.req_dob,
            is_active=True,
            is_suspended = False,
            suspension_end_time = datetime.now(),
            role = 'Accountant',
            is_superuser=False,
            profile_image=req_user.req_profile_image
        )
        new_user.save()
        RequestedUser.objects.filter(request_id=request_id).delete()
    except:
        messages.error(request, 'Error: Could not approve this user. Please try again later.')
        return HttpResponseRedirect('/users/administrator/unapproved_users/')

    success_string = 'User ' + new_employee_username + ' successfully approved.'
    messages.success(request, success_string)
    return HttpResponseRedirect('/users/administrator/unapproved_users/')

def reject_user(request):
    try:
        request_id = request.POST.get('request_id')
        RequestedUser.objects.filter(request_id=request_id).delete()
    except:
        messages.error(request, 'Error: Could not reject this user. Please try again later.')
        return HttpResponseRedirect('/users/administrator/unapproved_users/')

    messages.success(request, 'User successfully rejected.')
    return HttpResponseRedirect('/users/administrator/unapproved_users/')

####################################
#          Accountant Home         #
####################################

def render_accountant_page(request):
    current_admin = request.user
    return render(request, 'accountantMenu.html', {'current_admin': current_admin})

def render_accountant_view_accts_page(request):
    current_admin = request.user
    accounts = Account.objects.all()
    return render(request, 'accountantViewAccounts.html', {'current_admin': current_admin, 'accounts': accounts})

####################################
#           Manager Home           #
####################################

def render_manager_page(request):
    current_admin = request.user
    return render(request, 'managerMenu.html', {'current_admin': current_admin})

def render_manager_view_accts_page(request):
    current_admin = request.user
    accounts = Account.objects.all()
    return render(request, 'viewAccounts.html', {'current_admin': current_admin, 'accounts': accounts})

####################################
#            Login Page            #
####################################

def render_login_page(request):
    return render(request, 'main.html')

def login_user(request):
    login_username = request.POST.get('user_name')
    login_password = request.POST.get('user_password')

    current_user = authenticate(request, username=login_username, password=login_password)
    if current_user is not None and \
            (login_password == current_user.password) and \
            current_user.is_active:
        current_user.update_suspension()
        if current_user.get_suspended_status():
            print(login_username + " is still currently suspended")
            response = redirect('/users/')
            return response
        else:
            login(request, current_user)
            if current_user.role == 'Administrator':
                response = redirect('/users/administrator')
            elif current_user.role == 'Manager':
                response = redirect('/users/manager')
            else:
                response = redirect('/users/accountant')
    else:
        print('Wrong Username or Password.')
        response = redirect('/users/')

    return response

def logout_user(request):
    request.user = None
    return HttpResponseRedirect('/users')

####################################
#         Forgot Pass Page         #
####################################

def render_forgot_password_page(request):
    return render(request, 'forgotPassword.html')

def fp_get_creds(request):
    username = request.POST.get('curr_username')
    email = request.POST.get('curr_email')
    curr_user = verify_user_exists_via_email(username, email)
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
        response = redirect('/users/')
        return response

def verify_user_exists_via_email(username, email):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(username=username, email=email)
        return user
    except User.DoesNotExist:
        print('User not found!')
        pass


####################################
#     Render Exp. Password Page    #
####################################

def render_expired_passwords_page(request):
    current_date_time = datetime.now(timezone.utc)
    current_admin = request.user
    expired_pass_users = []
    users = User.objects.all()
    for user in users:
        time_elapsed_since_password_update = current_date_time - user.get_pass_dt()
        if time_elapsed_since_password_update.days >= PASSWORD_EXPIRY_THIRTY_DAYS:
            expired_pass_users.append(user)

    print(expired_pass_users)
    return render(request, 'viewExpiredPasswords.html', {'current_admin':current_admin, 'expired_pass_users':expired_pass_users})

def render_help_page(request):
    return render(request, 'Help.html')
##################################################################
#                    Unorganized Methods                         #
##################################################################

#calendar

def render_calendar_popup(request):

    c = calendar.HTMLCalendar(calendar.SUNDAY).formatmonth(2022,10)

    return render(request,'viewAccounts.html'), {
        "c": c,
    }

def generate_request_id():
    request_id = -2
    retry_count = 0
    retry = True
    request_id = random.randint(2000,2200)

    while(retry):
        try:
            if RequestedUser.objects.get(request_id=request_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return request_id

    request_id = -1
    return request_id

def generate_random_password():
    generated_password_length = 8
    special_characters = "!@#$%^&*()-+?_=,<>/"
    generated_password = ''
    generated_password = random.choice(string.ascii_lowercase)
    generated_password += random.choice(string.digits)
    generated_password += random.choice(special_characters)
    char = 3
    for char in range(generated_password_length-3):
        generated_password += secrets.choice(string.digits + special_characters + string.ascii_lowercase)

    return generated_password
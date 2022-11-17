from django.shortcuts import render
from accounts.models import Account, Account_Event_log
import random
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.utils.timezone import now, localtime
from django.template.loader import get_template


import pytz
from django.contrib import messages

from calendar import HTMLCalendar
import calendar 

from io import BytesIO

from xhtml2pdf import pisa




from django.http import HttpResponse
# Create your views here.

def render_create_chart_accts_page(request):
    return render(request, 'coa_main.html')

def render_event_log(request):
    events = Account_Event_log.objects.all()
    current_user = request.user
    return render(request, 'viewEventLog.html', {'events':events, 'current_user':current_user})

def render_viewaccounts_page(request):
    c = calendar.HTMLCalendar(calendar.SUNDAY).formatmonth(2022,1)
    accounts = Account.objects.all()
    current_admin = request.user
    return render(request, 'viewAccounts.html', {'c': c, 'accounts': accounts, 'current_admin': current_admin})

def search_account_results(request):
    pass

def render_delete_chart_accounts(request):
    return render(request, 'delete_coa.html')

def render_edit_chart_accounts(request):
    return render(request, 'edit_coa.html')

def create_chart_of_accounts(request):
    
    acct_id = generate_account_id()
    if acct_id == -1:
        messages.error(request, 'Error: Could not generate unique account ID for this Chart of Accounts. Please try again.')
        return render(request,'coa_main.html')

    try:
        new_account = Account  (
        account_id = acct_id,
        account_name = request.POST.get('acct_name'),
        credit_or_debit = request.POST.get('credit_or_debit'),
        account_desc = request.POST.get('acct_desc'),
        account_category = request.POST.get('acct_category'),
        account_sub_category = request.POST.get('acct_sc'),
        initial_balance = request.POST.get('init_bal'),
        debit_amount = request.POST.get('debit_amt'),
        credit_amount = request.POST.get('credit_amt'),
        current_balance = request.POST.get('acct_bal'),
        order = request.POST.get('order'),
        statement_type = request.POST.get('statement'),
        account_comment = request.POST.get('acct_comment'),
        is_active = True,
        user_id = request.user,
        dt_acct_creation = datetime.datetime.now()
    )
        new_account.save()
        create_event_log(request,acct_id,'CREATE CHART OF ACCOUNTS')

    except:
        messages.error(request, 'Error: Could not save this Chart of Accounts. Please try again.')
        return render(request,'coa_main.html')
    

    messages.success(request, 'Chart of Accounts with account ID: ' + str(acct_id) + ' successfully created.')
    return render(request,'coa_main.html')


def generate_account_id():
    acct_id = -2
    retry_count = 0
    retry = True
    acct_id = random.randint(1000,9999)

    while(retry):
        try:
            if Account.objects.get(account_id=acct_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return acct_id

    acct_id = -1
    return acct_id


def delete_chart_of_accounts(request):
    account_id = request.POST.get('account_id')

    try:
        Account.objects.get(account_id=account_id)
    except:
        messages.error(request, 'Error: Could find Chart of Accounts with account ID: ' + account_id + '.' + ' Please verify account ID and try again.')
        return render(request,'delete_coa.html')
    
    Account.objects.filter(account_id=account_id).delete()
    create_event_log(request,account_id,'DELETE CHART OF ACCOUNTS')
    messages.success(request, 'Chart of Accounts with account ID: ' + account_id + ' successfully deleted.')
    return render(request,'delete_coa.html')



def generate_event_log_id():
    acct_id = -2
    retry_count = 0
    retry = True
    acct_id = random.randint(10000,99999)

    while(retry):
        try:
            if Account_Event_log.objects.get(account_id=acct_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return acct_id

    acct_id = -1
    return acct_id





def create_event_log(request, account_id, event_desc):
    event_log_id = generate_event_log_id()
    
    try:
        new_event_log = Account_Event_log (
            event_id = event_log_id,
            user_source_id = request.user,
            account_source_id = account_id,
            action_description = event_desc
        )
        new_event_log.save()
        messages.success(request, 'New ' + event_desc + ' Event Created: ' + str(event_log_id))
    except:
        messages.error(request, 'Error: Could not save this event log. Please try again.')
    

def render_single_account(request, acct_id):
    curr_date_time = datetime.now()
    account = Account.objects.get(account_id=acct_id)
    return render(request, 'accountHTML.html', {'account': account, 'curr_date_time': curr_date_time})


def render_to_pdf(request, acct_id):
    account = Account.objects.get(account_id=acct_id)
    curr_date_time = datetime.now()
    context_dict = {'account': account, 'curr_date_time': curr_date_time}
    template = get_template('accountHTML.html')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

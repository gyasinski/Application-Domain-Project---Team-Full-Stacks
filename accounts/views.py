from django.shortcuts import render
from accounts.models import Account
import random
from django.http import HttpResponse
import datetime






from django.http import HttpResponse
# Create your views here.

def render_create_chart_accts_page(request):
    return render(request, 'coa_main.html')


def create_chart_of_accounts(request):
    
    acct_id = generate_account_id()
    if acct_id == -1:
        print('error!')
    else:
        print(acct_id)

    new_account = Account(
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



    return HttpResponse('Hello world!')


def generate_account_id():
    retry_count = 0
    retry = True
    acct_id = random.randint(0,10000000)

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

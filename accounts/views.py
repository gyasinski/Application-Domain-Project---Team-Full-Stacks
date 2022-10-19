from django.shortcuts import render
from accounts.models import Account
import random
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.contrib import messages
from django.views.generic import TemplateView, ListView


from django.http import HttpResponse
# Create your views here.

def render_create_chart_accts_page(request):
    return render(request, 'coa_main.html')

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
    messages.success(request, 'Chart of Accounts with account ID: ' + account_id + ' successfully deleted.')
    return render(request,'delete_coa.html')

class HomeSearchView(TemplateView):
    template_name = 'search_home.html'

class SearchResultsView(ListView):
    model = Account
    template_name = 'search_results.html'





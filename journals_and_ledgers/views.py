import random
from django.shortcuts import render
from accounts.models import Account
from journals_and_ledgers.models import JournalEntry
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
# Create your views here.


def render_journal_entry_page(request):
    accounts = Account.objects.all()
    return render(request, 'journalEntry.html', {'accounts': accounts, })

def submit_request_for_new_journal_entry(request):
    journal_entry_id = generate_journal_id()
    debit_account_id =  request.POST.get('debit_account_id')
    credit_account_id =  request.POST.get('credit_account_id')
    credit_account = Account.objects.get(account_id=credit_account_id)
    debit_account =  Account.objects.get(account_id=debit_account_id)
    debit_amount = request.POST.get('entry_debit')
    credit_amount = request.POST.get('entry_credit')

    try:
        requested_journal_entry = JournalEntry (
            journal_entry_id = journal_entry_id,
            account_debit_id =debit_account,
            account_credit_id = credit_account,
            debit_amount = debit_amount,
            credit_amount =  credit_amount,
            date_of_entry = datetime.now(),
            is_approved = False
            
        )
        requested_journal_entry.save()
    except Exception as e:
        print(e)
        messages.error(request, 'Error, could not send request at this time, Please try again later.')
        return HttpResponseRedirect('/journals_ledger/journal_entry')

    messages.success(request, 'Success! Request sent with Request ID: ' + str(journal_entry_id) + '. ')
    return HttpResponseRedirect('/journals_ledger/journal_entry')


def render_unapproved_entries_page(request):
    unapproved_entries = JournalEntry.objects.all()
    current_admin = request.user
    return render(request, 'requestedEntries.html', {'unapproved_users': unapproved_entries, 'current_admin':current_admin} )




def generate_journal_id():
    request_id = -2
    retry_count = 0
    retry = True
    request_id = random.randint(3000,3300)

    while(retry):
        try:
            if JournalEntry.objects.get(request_id=request_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return request_id
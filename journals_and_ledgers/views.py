import random
from django.shortcuts import render
from accounts.models import Account
from journals_and_ledgers.models import JournalEntry, TransactionError
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
# Create your views here.


def render_journal_entry_page(request):
    curr_user = request.user
    return render(request, 'journalEntry.html', {'curr_user' : curr_user})

def submit_request_for_new_journal_entry(request):
    journal_entry_id = generate_journal_id()
    initial_comment = request.POST.get('entry_description')
    debit_account_id = request.POST.get('debit_account_id')
    credit_account_id = request.POST.get('credit_account_id')
    credit_account = Account.objects.get(account_id=credit_account_id)
    debit_account = Account.objects.get(account_id=debit_account_id)
    debit_amount = request.POST.get('entry_debit')
    credit_amount = request.POST.get('entry_credit')

    try:
        requested_journal_entry = JournalEntry (
            journal_entry_id = journal_entry_id,
            user_submission_id = request.user,
            initial_entry_description = initial_comment,
            account_debit_id = debit_account,
            account_credit_id = credit_account,
            debit_amount = debit_amount,
            credit_amount =  credit_amount,
            date_of_entry = datetime.now(),
        )
        requested_journal_entry.save()
    except Exception as e:
        transactError = TransactionError(
        error_id = generate_transactionerror_id(),
        error_date_time = datetime.now(),
        error_desc = str(e)
    )
        transactError.save()
        messages.error(request, 'Error, could not send request at this time, Please try again later.')
    
        return HttpResponseRedirect('/journals_ledger/journal_entry')

    messages.success(request, 'Success! Your request has been sent and is awaiting approval. Journal Entry ID: ' + str(journal_entry_id) + '. ')
    return HttpResponseRedirect('/journals_ledger/journal_entry')


def render_unapproved_entries_page(request):
    journal_entries = JournalEntry.objects.all()
    curr_user = request.user
    return render(request, 'requestedEntries.html', {'journal_entries': journal_entries, 'curr_user': curr_user} )



def perform_transactions(debit_account, credit_account, journal):
    if journal.credit_amount > credit_account.current_balance:
        transactError = TransactionError(
        error_id = generate_transactionerror_id(),
        error_date_time = datetime.now(),
        error_desc = str('Not enough cash to credit from. Please contact an administrator...and an accountant.')
    )
        transactError.save()
    else:
        credit_account.current_balance -= journal.credit_amount
        debit_account.current_balance += journal.debit_amount
        debit_account.save()
        credit_account.save()
        

def commit_journal_entry_approval(request):
    curr_user = str(request.user)
    try:
        journal_id = request.POST.get('journal_id')
        curr_journal = JournalEntry.objects.get(journal_entry_id=journal_id)
        curr_journal.approve_journal()
        curr_journal.set_approver_id(curr_user)
        perform_transactions(curr_journal.account_credit_id, curr_journal.account_debit_id,curr_journal)
        curr_journal.save()
    except Exception as e:
        transactError = TransactionError(
        error_id = generate_transactionerror_id(),
        error_date_time = datetime.now(),
        error_desc = str(e)
    )
        transactError.save()
        messages.error(request, 'Error, could not approve journal at this time, Please try again later.')


    messages.success(request, 'Success! Journal has been approved and transactions have been completed.')
    return HttpResponseRedirect('/journals_ledger/manager/unapproved_entries/')


def reject_journal_entry(request):
    try:
        journal_id = request.POST.get('journal_id')
        JournalEntry.objects.filter(journal_entry_id=journal_id).delete()
    except Exception as e:
        print(e)
        transactError = TransactionError(
        error_id = generate_transactionerror_id(),
        error_date_time = datetime.now(),
        error_desc = str(e)
    )
        transactError.save()
        messages.error(request, 'Error: Could not delete this journal. Please try again later.')
        return HttpResponseRedirect('/journals_ledger/manager/unapproved_entries/')

    messages.success(request, 'Journal successfully rejected.')
    return HttpResponseRedirect('/journals_ledger/manager/unapproved_entries/')



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

def generate_transactionerror_id():
    error_id = -2
    retry_count = 0
    retry = True
    error_id = random.randint(4000,4100)

    while(retry):
        try:
            if TransactionError.objects.get(error_id=error_id):
                retry_count += 1
                if retry_count == 10:
                    retry = False
        except:
            return error_id
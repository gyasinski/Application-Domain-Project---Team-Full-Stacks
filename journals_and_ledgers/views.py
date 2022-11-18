import random
from django.shortcuts import render
from accounts.models import Account
from journals_and_ledgers.models import JournalEntry, TransactionError
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
import json
from django.core.files.storage import FileSystemStorage
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
    
    #to attach a file
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.filename, file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'journalEntry.html', {
            'uploaded_file_url': uploaded_file_url
        })

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
            file = file,
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


def save_rejected_journal_entry_id(request):
    request.session['curr_rejected_journal'] = request.POST.get('journal_id')
    print(request.session.get('curr_rejected_journal'))
    return HttpResponse(
        request.session.get('curr_rejected_journal')
    )


def reject_journal_entry(request):
    
    try:
        curr_user = str(request.user)
        curr_rejected_journal_id = request.session.get('curr_rejected_journal')
        rej_comment = request.POST.get('rejection_comment')
        curr_journal = JournalEntry.objects.get(journal_entry_id=curr_rejected_journal_id)
        curr_journal.reject_journal()
        curr_journal.set_approver_id(curr_user)
        curr_journal.add_rejection_comment(rej_comment)
        curr_journal.save()
    except Exception as e:
        messages.error(request, 'Error: Could not delete this journal. Please try again later.')
        return HttpResponseRedirect('/journals_ledger/manager/unapproved_entries/')
    
    messages.success(request, 'Journal successfully rejected.')

    journal_entries = JournalEntry.objects.all()
    curr_user = request.user
    return render(request, 'requestedEntries.html', {'journal_entries': journal_entries, 'curr_user': curr_user} )
    

   

# Karens Merge ##################################

def render_approved_entries_page(request):
    approved_entries = JournalEntry.objects.all()
    current_admin = request.user
    return render(request, 'approvedEntries.html', {'approved_users': approved_entries, 'current_admin':current_admin} )

## rejected journal entries ##

def render_rejected_entries_page(request):
    rejected_entries = JournalEntry.objects.all()
    current_admin = request.user
    return render(request, 'rejectedEntries.html', {'rejected_users': rejected_entries, 'current_admin':current_admin} )

## search venues ##

def search_journals_page(request):
    if request.method == "POST":
        searched= request.POST('searched')
    journals= JournalEntry.objects.filter(journal_entry_id__contains= searched)
    journals= JournalEntry.objects.filter(debit_amount__contains= searched)
    journals= JournalEntry.objects.filter(date_of_entry__contains= searched)

    return render(request,'search_journals.html', {'searched': searched, 'journals': journals} )

# end Karens merge ########################################################################
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
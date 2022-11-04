from enum import unique
from django.db import models
from accounts.models import Account
from users.models import User

# Create your models here.




class JournalEntry(models.Model):
    journal_entry_id = models.IntegerField(unique=True, primary_key=True)
    user_submission_id = models.ForeignKey(User, on_delete=models.CASCADE)
    initial_entry_description = models.CharField(max_length=200)
    date_of_entry = models.DateField(auto_now_add=True)
    account_debit_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_debit_id')
    account_credit_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_credit_id')
    debit_amount = models.DecimalField(max_digits=19, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=19, decimal_places=2)
    journal_comment = models.TextField(max_length=200)
    is_approved = models.BooleanField(default=False)
    approver_id = models.CharField(default='Unapproved', max_length=50)

    def approve_journal(self):
        self.is_approved = True

    def set_approver_id(self, approver_id):
        self.approver_id = approver_id


class TransactionError(models.Model):
    error_id = models.IntegerField(unique=True, primary_key=True)
    error_date_time = models.DateTimeField(auto_now_add=True)
    error_desc = models.CharField(max_length=1000)




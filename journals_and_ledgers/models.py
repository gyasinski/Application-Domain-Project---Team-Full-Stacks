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
    is_rejected = models.BooleanField(default=False)
    approver_id = models.CharField(default='Unapproved', max_length=50)
    reject_comment = models.TextField(max_length=200, default="This journal entry has not been rejected yet or was approved.")

    #for file upload
    file = models.FileField()

    def approve_journal(self):
        self.is_approved = True
        self.is_rejected = False

    def set_approver_id(self, approver_id):
        self.approver_id = approver_id

    def reject_journal(self):
        self.is_rejected = True
        self.is_approved = False

    def add_rejection_comment(self, reject_comment):
        self.reject_comment = reject_comment

class TransactionError(models.Model):
    error_id = models.IntegerField(unique=True, primary_key=True)
    error_date_time = models.DateTimeField(auto_now_add=True)
    error_desc = models.CharField(max_length=1000)




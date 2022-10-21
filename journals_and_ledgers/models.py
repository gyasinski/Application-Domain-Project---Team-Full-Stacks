from enum import unique
from django.db import models
from accounts.models import Account

# Create your models here.


class JournalEntry(models.Model):
    journal_entry_id = models.IntegerField(unique=True, primary_key=True)
    date_of_entry = models.DateField(auto_now_add=True)
    account_debit_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_debit_id')
    account_credit_id = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_credit_id')
    debit_amount = models.DecimalField(max_digits=19, decimal_places=10)
    credit_amount = models.DecimalField(max_digits=19, decimal_places=10)
    is_approved = models.BooleanField(default=False)


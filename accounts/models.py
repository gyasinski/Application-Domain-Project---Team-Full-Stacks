from tkinter.font import NORMAL
from django.db import models
from users.models import User
# Create your models here.



class Account(models.Model):
    account_id = models.IntegerField(primary_key=True, unique=True)
    account_name = models.CharField(max_length=30, unique=True)
    CREDIT = 'Credit'
    DEBIT = 'Debit'
    NORMAL_SIDE = [
        (CREDIT, 'Credit'),
        (DEBIT, 'Debit'),
    ]
    credit_or_debit = models.CharField(
        max_length = 6,
        choices = NORMAL_SIDE,
    )
    account_desc = models.TextField(max_length=200)
    account_category = models.CharField(max_length=15)
    account_sub_category = models.CharField(max_length=20)
    initial_balance = models.DecimalField(max_digits=19, decimal_places=10)
    debit_amount = models.DecimalField(max_digits=19, decimal_places=10)
    credit_amount = models.DecimalField(max_digits=19, decimal_places=10)
    current_balance = models.DecimalField(max_digits=19, decimal_places=10)
    dt_acct_creation = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('users.user',on_delete=models.CASCADE)
    account_comment = models.TextField(max_length=200)
    INCOME_STATEMENT = 'IS'
    BALANCE_SHEET = 'BS'
    RETAINED_EARNINGS_STATEMENT = 'RES'
    STATEMENT = [
        (INCOME_STATEMENT, 'Income Statement'),
        (BALANCE_SHEET, 'Balance Sheet'),
        (RETAINED_EARNINGS_STATEMENT, 'Retained Earnings Statement'),
    ]
    statement_type = models.CharField(
        max_length=3,
        choices=STATEMENT,
    )
    is_active = models.BooleanField(default=True)




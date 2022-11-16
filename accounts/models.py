from enum import unique
from random import choices
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

    ASSET = 'Asset'
    LIABILITY = 'Liability'
    EXPENSES = 'Expenses'
    EQUITY = 'Equity'
    REVENUE = 'Revenue'
    ACCT_CATEGORY = [
        (ASSET, 'Asset'),
        (LIABILITY, 'Liability'),
        (EXPENSES, 'Expenses'),
        (EQUITY, 'Equity'),
        (REVENUE, 'Revenue'),
    ]

    account_category = models.CharField(
        max_length=9,
        choices=ACCT_CATEGORY,
    )


    account_sub_category = models.CharField(max_length=20)
    initial_balance = models.DecimalField(max_digits=19, decimal_places=2)
    debit_amount = models.DecimalField(max_digits=19, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=19, decimal_places=2)
    current_balance = models.DecimalField(max_digits=19, decimal_places=2)
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
        max_length=27,
        choices=STATEMENT,
    )

    CASH = 'Cash'
    MARKET_SECURITIES = 'Marketable Securities'
    ACCOUNTS_REC = 'Accounts Recievable'
    INVENTORY = 'Inventory'
    FIXED_ASSETS = 'Fixed Assets'
    GOODWILL = 'Goodwill'

    ORDER_OF_LIQUIDITY = [
        (CASH, 'Cash'),
        (MARKET_SECURITIES, 'Market Securities'),
        (ACCOUNTS_REC, 'Accounts Recievable'),
        (INVENTORY, 'Inventory'),
        (FIXED_ASSETS, 'Fixed Assets'),
        (GOODWILL, 'Goodwill'),
    ]

    order = models.CharField(
        max_length = 21,
        choices = ORDER_OF_LIQUIDITY,
    )




    is_active = models.BooleanField(default=True)




class Account_Event_log(models.Model):
    event_id = models.IntegerField(unique=True, primary_key=True)
    user_source_id = models.ForeignKey('users.user', on_delete=models.CASCADE) #Shouldnt be able to edit this, so no deletion
    account_source_id = models.IntegerField()
    action_description = models.CharField(max_length=100)
    event_date = models.DateTimeField(auto_now_add=True)






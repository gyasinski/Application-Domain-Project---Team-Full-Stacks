# Generated by Django 4.1.1 on 2022-10-01 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_account_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='statement_type',
            field=models.CharField(choices=[('IS', 'Income Statement'), ('BS', 'Balance Sheet'), ('RES', 'Retained Earnings Statement')], default='IS', max_length=3),
        ),
    ]
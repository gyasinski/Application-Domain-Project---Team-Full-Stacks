# Generated by Django 4.1.1 on 2022-10-01 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_account_is_active_alter_account_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='credit_or_debit',
            field=models.CharField(choices=[('Credit', 'Credit'), ('Debit', 'Debit')], default='Credit', max_length=6),
            preserve_default=False,
        ),
    ]

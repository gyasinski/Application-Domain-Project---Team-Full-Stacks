# Generated by Django 4.1.1 on 2022-10-01 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_account_statement_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]

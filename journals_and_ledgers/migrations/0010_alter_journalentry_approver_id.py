# Generated by Django 4.1.1 on 2022-11-04 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals_and_ledgers', '0009_alter_journalentry_credit_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='approver_id',
            field=models.CharField(default='Unapproved', max_length=50),
        ),
    ]

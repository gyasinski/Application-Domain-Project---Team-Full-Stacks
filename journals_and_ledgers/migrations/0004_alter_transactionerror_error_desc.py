# Generated by Django 4.1.1 on 2022-11-02 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals_and_ledgers', '0003_transactionerror_journalentry_journal_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionerror',
            name='error_desc',
            field=models.CharField(max_length=1000),
        ),
    ]

# Generated by Django 4.1.1 on 2022-11-04 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals_and_ledgers', '0007_journalentry_approver_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='debit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
# Generated by Django 4.1.1 on 2022-11-04 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals_and_ledgers', '0008_alter_journalentry_debit_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='credit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]

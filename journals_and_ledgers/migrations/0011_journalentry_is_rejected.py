# Generated by Django 4.1.1 on 2022-11-14 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals_and_ledgers', '0010_alter_journalentry_approver_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]

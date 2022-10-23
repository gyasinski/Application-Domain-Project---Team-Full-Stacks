# Generated by Django 4.1.1 on 2022-10-22 23:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_account_event_log_account_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_event_log',
            name='event_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

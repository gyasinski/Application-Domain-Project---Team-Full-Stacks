# Generated by Django 4.1.1 on 2022-10-08 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_date_of_birth_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password_init_dt',
            new_name='password_date_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_role',
        ),
    ]
# Generated by Django 4.1.1 on 2022-10-21 17:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_user_suspension_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='suspension_end_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 21, 13, 18, 12, 994343)),
        ),
    ]
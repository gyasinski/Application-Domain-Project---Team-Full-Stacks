# Generated by Django 4.1.1 on 2022-10-09 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestedUser',
            fields=[
                ('request_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('req_first_name', models.CharField(max_length=50)),
                ('req_last_name', models.CharField(max_length=50)),
                ('req_email', models.EmailField(max_length=50, null=True, verbose_name='email')),
                ('req_address', models.CharField(max_length=50)),
                ('req_apartment_or_suite_num', models.CharField(max_length=50)),
                ('req_city', models.CharField(max_length=50)),
                ('req_state', models.CharField(max_length=50)),
                ('req_zip_code', models.CharField(max_length=50)),
                ('req_country', models.CharField(max_length=50)),
                ('req_dob', models.DateField()),
                ('req_profile_image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-10 21:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='A first name of user', max_length=100)),
                ('last_name', models.CharField(help_text='A last name of user', max_length=100)),
                ('address', models.CharField(help_text='Address of the user', max_length=600)),
                ('contact', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9999999999'. Up to 10 digits allowed.", regex='^\\+?1?\\d{9,10}$')])),
                ('email_id', models.EmailField(max_length=200)),
                ('website', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]

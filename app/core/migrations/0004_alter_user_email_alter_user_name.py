# Generated by Django 4.1a1 on 2022-06-05 12:04

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator], verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, validators=[core.models.MinLengthValidatorNoSpace(3, 'name must be minimum 3 charector long'), django.core.validators.MaxLengthValidator(30, 'name should not be more than 30 charector long.'), django.core.validators.RegexValidator('^[a-zA-Z ]+$', 'Only letters and spaces are allowed.')], verbose_name='full name'),
        ),
    ]
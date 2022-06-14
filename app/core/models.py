
import random
from django.db import models
import string
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator, MaxLengthValidator
from core.user_manager import UserManager


class MinLengthValidatorNoSpace(MinLengthValidator):
    def clean(self, x):
        """
        overridding clean method to strip spaces both side of string then check the len
        """
        x = x.strip()
        return len(x)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_("full name"), default='', max_length=30,
                            validators=[
                                MinLengthValidatorNoSpace(
                                    3, 'name must be minimum 3 charector long'),
                            MaxLengthValidator(
                                30, 'name should not be more than 30 charector long.'),
                                RegexValidator(r'^[a-zA-Z ]+$',
                                               'Only letters and spaces are allowed.'),
                            ])
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        validators=[EmailValidator, ]
    )

    slug = models.SlugField(_("slug"), default="", unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def get_absolute_url(self):
        return reverse("me", kwargs={"slug": self.slug})
    

    def save(self, *args, **kwargs):
        # slug with name and 4 char random string
        self.slug = slugify(self.name) + ''.join( random.choice(string.ascii_lowercase) for i in range(4)) 
        return super().save(*args, **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"

        return self.is_admin

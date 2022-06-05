
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from core.user_manager import UserManager


alphabet_validator = RegexValidator(
    regex='[a-zA-Z]', message="Only alphabet charecters are allowed.")


class User(AbstractBaseUser):
    name = models.CharField(_("full name"), max_length=50,
                            validators=[alphabet_validator])
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )

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

    @property
    def is_staff(self):
        "Is the user a member of staff?"

        return self.is_admin

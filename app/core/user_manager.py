import re
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.forms import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, name, email,  password=None, **extra_fields):
        """
        Creates and saves a User with the given name, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            **extra_fields
        )

        
        regex_pattern="^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,16}$"
        
        if not re.search(regex_pattern, password):
            raise ValidationError(message="Enter 8 or longer digit complex password.")

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, name, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given nmae, email and password.
        """
        user = self.create_user(
            name=name,
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

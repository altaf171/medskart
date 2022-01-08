from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db.models.fields import BooleanField, CharField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

#-----------User manager---------------------------
class UserManager(BaseUserManager):
    def create_user(self, mobile, password=None, **extra_fields):
        """creates and saves a new user"""

        if not mobile:
            raise ValueError(" user must have an mobile number number")

        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    """Custom user model supports creating user with mobile number"""
    mobile = PhoneNumberField(unique=True)
    password = CharField(max_length=255)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def __str__(self):
        return self.mobile
      


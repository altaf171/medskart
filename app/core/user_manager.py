from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, email,  password=None):
        """
        Creates and saves a User with the given name, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name = name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        """
        Creates and saves a superuser with the given nmae, email and password.
        """
        user = self.create_user(
            email,
            name=name,
            password=password,
             
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
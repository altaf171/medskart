from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_succesfull(self):
        """ test that user can be created with email, name and password """

        name = 'your bro'
        email = 'yourbro@look.there'
        password = 'Test67#po'

        user = User.objects.create_user(name=name, email=email, password=password)
        # user = User(name=name, email=email)
        # user.set_password(password)
        # user.full_clean()
        # self.assertRaises (ValidationError, user.full_clean)
        user.save()

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_fail_invalid_name(self):
        """test that creating user fail with invalid name """
        name = '#your bro' # invalid name
        email = 'yourbro@look.there'
        password =  'Test67#po'

        with self.assertRaises(ValidationError):
            user = User(name=name, email=email)
            user.set_password(password)
            user.full_clean()

    def test_fail_invalid_email(self):
        """test that creating user fail with invalid name """
        name = 'your bro' 
        email = 'yourbro look.there' # invalid email
        password =  'Test67#po'

        with self.assertRaises(ValidationError):
            user = User(name=name, email=email)
            user.set_password(password)
            user.full_clean()

    def test_fail_insecure_password(self):
        """test that creating user fail with invalid name """
        name = 'your bro' 
        email = 'yourbro@look.there'
        # password = 'WoofGirl@24' 
        password = '8524' #insecure password

        with self.assertRaises(ValidationError):
           User.objects.create_user(name=name, email=email, password=password)
    
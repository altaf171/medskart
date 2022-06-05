from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user_succesfull(self):

        """ test that user can be created with email, name and password """

        name = 'your bro'
        email = 'yourbro@look.there'
        password = 'Test67#'

        # user = User.objects.create_user(name=name, email=email, password=password)
        user = User(name=name, email=email)
        user.set_password(password)
        user.full_clean()
        # self.assertRaises (ValidationError, user.full_clean)
        user.save()

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    # def test_user_create_fail_with_simple_password(self):
    #     name = 'your bro'
    #     email = 'yourbro@look.there'
    #     password = '1234'
    #     user = User.objects.create_user(name=name, email=email, password=password)
    #     self.assertEquals(user.email, email)
    #     self.assertTrue(user.check_password(password))
    

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTest(TestCase):
    def create_user_with_email_succesfull(self):

        """ test that user can be created with email, name and password """

        name = 'your bro'
        email = 'yourbro look.there'
        password = 'Test67#'

        user = get_user_model().objects.create_user(
            name=name, email=email, password=password)

        print(user.name)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

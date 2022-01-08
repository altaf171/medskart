from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def test_create_user_with_mobile_successful(self):
        """Test that creating an user with mobile number is working"""
        mobile = '9178125678'
        password = 'Testpass@123'
        user = get_user_model().objects.create_user(mobile=mobile, password=password)
        self.assertEqual(user.mobile, mobile)
        self.assertTrue(user.check_password(password))

    def test_new_user_mobile_no_invalid_phone(self):
        """Testing creating user with no phone raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'Testpass@123')
    
    
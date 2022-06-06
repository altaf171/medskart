import email
import imp
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('user:create')


def create_user(**prams):
    return get_user_model().objects.create(**prams)


class PublicUserAPITests(APITestCase):
    """ Test user api (public) (❁´◡`❁)  """
    def test_create_user(self):
        """ 
        Ensure that can create new user with
        valid data
        """
        data = {
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        }
       
        response = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count, 1)
        self.assertEqual(get_user_model().objects.get().email, data["email"])
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        """
        ☆*: .｡. o(≧▽≦)o .｡.:*☆
        test fails if user that we are trying to create is already exists
        \(@^0^@)/
        """
        data = {
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        }

    
        response = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
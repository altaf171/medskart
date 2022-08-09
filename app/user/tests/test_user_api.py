from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('user:create')
# JWT token url
TOKEN_URL = reverse('user:token_obtain_pair')

PROFILE_URL = reverse("user:profile")


def create_user(**prams):
    return get_user_model().objects.create(**prams)


class PublicUserAPITests(APITestCase):
    """ Test user api (public) (❁´◡`❁)  """

    def setUp(self):
        self.client = APIClient()

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
        # self.assertEqual(get_user_model().objects.count, 1)
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
        # creating user
        create_user(**data)
        # testing if user already exists
        response = self.client.post(CREATE_USER_URL, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ 🧪 Test that password must be 8 or more charector long 🤿 """
        data = {
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You"
        }
        response = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # check if user is got created
        user_exists = get_user_model().objects.filter(
            email=data["email"]).exists()
        self.assertFalse(user_exists)

    def test_token_created(self):
        """ Ensure that token is created for user """
        data = {
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        }

        # creating user before login test to get token
        create_response = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        login_data = {
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        }

        response = self.client.post(
            TOKEN_URL, login_data)

        # print(response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_token_invalid_credentials(self):
        """ Ensure that no token is given user with wrong credentials"""
        data = {
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        }

        # creating user before login test to get token
        create_response = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        login_data = {
            "email": "yourboy24@here.now",
            "password": "they&Yoing1"
        }
        response = self.client.post(TOKEN_URL, login_data)

        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_token_non_existing_user(self):
        """test that no token is generated when user does not exists"""
        login_data = {
            "email": "me24@here.now",
            "password": "they&Doing1"
        }
        response = self.client.post(TOKEN_URL, login_data)

        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_token_blank_pass_field(self):
        """test that no token is generated when password filed is blank"""
        login_data = {
            "email": "yourboy24@here.now",
            "password": ""
        }
        response = self.client.post(TOKEN_URL, login_data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """test that authentication is required for user to see their profile"""

        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """ Test those api resquest that are authenticated """

    def setUp(self):
        self.user = create_user(**{
            "name": "your boy",
            "email": "yourboy24@here.now",
            "password": "Me&You&noting1"
        })
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """ test that retrieving profile for user """

        response = self.client.get(PROFILE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "name": self.user.name,
            "email": self.user.email
        })

    def test_me_post_not_allowed(self):
        """ Test that post method is not allowed on user """
        response = self.client.post(PROFILE_URL, {})
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """ Test that user profile get updated """
        data  = {"name":"me mine", "password":"Me#My123*"}
        response = self.client.patch(PROFILE_URL,data)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, data["name"])
        self.assertTrue(self.user.check_password(data["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
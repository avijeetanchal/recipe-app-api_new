from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
# we use this to make request to our API and check response.

from rest_framework import status

# CREATE A HELPER FUNC OR CONSTANT VARIBALE FOR OUR URL
CREATE_USER_URL = reverse('user:create')# constant VARIBALE

TOKEN_URL = reverse('user:token')

# helper class
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """test the users API public"""

    def setUp(self):
        self.client = APIClient()


    # test user crated success
    def test_create_valid_user_success(self):
        """TEST creating user with valid payload is success"""
        payload = {
            'email': 'test@testing.com',
            'password': 'test123',
            'name': 'Test '
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data) # getting users which is created
        self.assertTrue(user.check_password(payload['password'])) # checking password correct we input is correct
        self.assertNotIn('password',res.data) # password should not return


    def test_user_exits(self):
        """test user already exit if new create"""
        payload = {
            'email': 'test@testing.com',
            'password': 'test123',
            'name': 'Test '
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        """Password should not be less than 5 charaters"""
        payload = {
            'email': 'test@testing.com',
            'password': 'pw',
            'name': 'Test '
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

#################   testing token authentication

    def test_create_token_for_user(self):
        """TEST THAT TOKEN IS CREATED FOR THE USER"""
        payload = {
            'email': 'test@testing.com',
            'password': 'test123',
            'name': 'Test '
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload) # store response

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        """test that token is not created if invalid creds are passed"""
        create_user(email='test@testing.com',password='test123')
        payload = {
            'email': 'test@testing.com',
            'password': 'test123',
            #'name': 'Test '
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """TEST token not created if user doesnt exists"""
        payload = {
             'email': 'test@testing.com',
             'password': 'test123',
             #'name': 'Test '
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missin_field(self):
        """test that email and pass required"""
        res = self.client.post(TOKEN_URL, {'email':'one','password':''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

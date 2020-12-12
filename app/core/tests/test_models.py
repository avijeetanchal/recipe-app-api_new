from django.test import TestCase

from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test2@testing.com',password='test123'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)



class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """TEST CREATIGN A NEW USER WITH EMAIL"""
        email = 'test@testing.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email,email)
        ## email in created user object is same as email
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalised(self):
        """test that email is in small caps"""
        email = 'test@TESING.COM'
        user = get_user_model().objects.create_user(email,'test_passwrd')

        self.assertEqual(user.email, email.lower())


    def test_new_user_invalid_email(self):
        """test creating user woth no email, then raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'test_passwrd')


    def test_create_new_super_user(self):
        """testing creation of is staff and is super user"""
        user = get_user_model().objects.create_superuser(
            'test@testing.com','test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user = sample_user(), # () to create new user for test
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

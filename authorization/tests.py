from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction
from .models import CustomUser

# Create your tests here.
class CreateUserManagersTest(TestCase):
    
    @classmethod
    def setUpTestData(cls) -> None:
        #Getting customuser model
        cls.User = get_user_model()
    ########################################################################################################################################
    # CREATE USER
    def test_create_user(self):
        '''Checks creating user in different ways'''

        # Creating new user
        self.User.objects.create_user(email='test@gmail.com', username = 'Vitalii', password = '1234')
        user = self.User.objects.get(username = 'Vitalii')
        # ---------------------------------------------------------------------------------------------------

        # Checks input data
        self._check_input_data(user, 'test@gmail.com', 'Vitalii', '1234')
        # ----------------------------------------------------------------

        # Checks is it user without any permissons.
        self._is_without_any_permissions(user)
        # ----------------------------------------

        # Attempts to create a user with incorrect / incomplete data
        self._create_user_with_incorrect_or_incomplete_data()
        # ----------------------------------------------------------


        # Attempt to create a user with correct data
        self.assertTrue(self.User.objects.create_user(email = 'aoiwudh@gmail.com', username = 'Vitaliii', password = '1234'))

    def _create_user_with_incorrect_or_incomplete_data(self):


        self.assertTrue(self._create_user_with_existing_email())
        self.assertTrue(self._create_user_with_existing_nickname())
        

        with self.assertRaises(ValidationError):
            self.User.objects.create_user()
        with self.assertRaises(ValidationError):
            self.User.objects.create_user(email='321123@gmail.com')
        with self.assertRaises(ValidationError):
            self.User.objects.create_user(email='', password='321', username = 'Anton')

    def _is_without_any_permissions(self, user: CustomUser):
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_superuser)

    def _create_user_with_existing_email(self):
        try:
            with transaction.atomic():
                self.User.objects.create_user(email='test@gmail.com', username = 'Vitaliii', password = '1234')
        except IntegrityError:
            return True
        else:
            return False

    def _create_user_with_existing_nickname(self):
        try:
            with transaction.atomic():
                self.User.objects.create_user(email='testt@gmail.com', username = 'Vitalii', password = '1234')
        except IntegrityError:
            return True
        else:
            return False

    ########################################################################################################################################
    # CREATE SUPERUSER
    def test_create_superuser(self):
        '''Check creating superuser in different ways'''

        # Creating new superuser
        self.User.objects.create_superuser(email='superuser@gmail.com', username = 'super', password = '1234')
        superuser = self.User.objects.get(username = 'super')
        # ---------------------------------------------------------------------------------------------------

        # Checks input data
        self._check_input_data(superuser, 'superuser@gmail.com', 'super', '1234')
        # ----------------------------------------------------------------

        # Checks is it user without permissons.
        self._is_with_permissions(superuser)
        # ----------------------------------------

        # Attempts to create a superuser with incorrect / incomplete data
        self._create_superuser_with_incorrect_or_incomplete_data()
        # ---------------------------------------------------------------

        # Attempt to create a user with correct data
        self.assertTrue(self.User.objects.create_superuser(email = 'aoiwuddsah@gmail.com', username = 'I`M SUPER', password = '1234'))

    def _create_superuser_with_incorrect_or_incomplete_data(self):
        self.assertTrue(self._create_superuser_with_existing_email())
        self.assertTrue(self._create_superuser_with_existing_nickname())

        with self.assertRaises(ValidationError):
            self.User.objects.create_superuser()
        with self.assertRaises(ValidationError):
            self.User.objects.create_superuser(email='321123@gmail.com')
        with self.assertRaises(ValidationError):
            self.User.objects.create_superuser(email='', password='321', username = 'Anton')

    def _is_with_permissions(self, user: CustomUser):
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)

    def _create_superuser_with_existing_email(self):
        try:
            with transaction.atomic():
                self.User.objects.create_superuser(email='superuser@gmail.com', username = 'superr', password = '1234')
        except IntegrityError:
            return True
        else:
            return False

    def _create_superuser_with_existing_nickname(self):
        try:
            with transaction.atomic():
                self.User.objects.create_superuser(email='superuserr@gmail.com', username = 'super', password = '1234')
        except IntegrityError:
            return True
        else:
            return False
            
    def _check_input_data(self, user: CustomUser, correct_email: str,
                                correct_username: str, correct_password: str):
        self.assertEqual(user.email, correct_email)
        self.assertEqual(user.username, correct_username)
        self.assertTrue(user.check_password(correct_password))
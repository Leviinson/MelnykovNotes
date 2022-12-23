from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
# Create your models here.

class AccountManager(BaseUserManager):


    def create_user(self, email: str = '', username: str = '', password: str = ''):
        if not all(x for x in (email, username, password)):
            raise ValidationError('This field is required [!]')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str = '', username: str = '', password: str = ''):
        if not all(x for x in (email, username, password)):
            raise ValidationError('This field is required [!]')

        user = self.create_user(
            email = email,
            username = username,
            password = password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default = uuid4, unique = True)
    email = models.EmailField(unique = True, verbose_name = 'User`s email')
    username = models.CharField(max_length = 30, unique = True, verbose_name = 'User`s nickname', db_index = True)
    biography = models.CharField(max_length = 300, blank = True)
    picture = models.ImageField(upload_to = 'user_picture/%Y/%m/%d', default = '', blank = True, null = False)
    date_joined = models.DateTimeField(auto_now_add = True, verbose_name = 'Date joined')
    last_login = models.DateTimeField(auto_now = True, verbose_name = 'Last login')
    is_active = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    friends = models.ManyToManyField("self", blank = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )
    objects = AccountManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = "user's"
        ordering = ['date_joined']
        get_latest_by = ['date_joined']
        
    def __repr__(self):
        return f"[{self.email} -- {self.last_login}]"

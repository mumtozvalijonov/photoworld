from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from account.managers import UserManager


class Account(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=50)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    bio = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='images/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

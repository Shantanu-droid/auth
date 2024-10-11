from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    '''manager for user'''

    def create_user(self, email, password=None, **kwargs):
        '''create save and return a new user'''
        if not email:
            raise ValueError('user must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password=None, **kwargs):
        '''create and return a new superuser'''
        super_user = self.create_user(email=email, password=password)
        super_user.is_staff = True
        super_user.is_superuser = True

        super_user.save(using=self._db)
        
        return super_user
    
class User(AbstractBaseUser, PermissionsMixin):
    '''user in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
# models.py
import random
from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class OTPManager(models.Manager):
    '''manager for user'''

    @staticmethod
    def generate_otp():
        '''generate a random int of 6 digits'''
        return random.randint(100000, 999999)

    def create_otp(self, user, **kwargs):
        '''create save and return a new user'''
        if not user:
            raise ValueError('user cannot be empty')
        otp = self.model(
            user=user, otp=OTPManager.generate_otp(), **kwargs)
        otp.save(using=self._db)
        return otp

class OTP(models.Model):
    '''OTP class for otp generated by users'''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = OTPManager()

    def is_valid(self):
        """Check if OTP is still valid."""
        return datetime.now() <= \
            self.created_at + timedelta(minutes=settings.OTP_VALID_UNTIL_MINS)

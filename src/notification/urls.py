'''
URL mappings for the user APIs
'''
from django.urls import path
from .views import SendRecoveryMail


app_name = 'notification'

urlpatterns = [
    path('send-account-recovery/', SendRecoveryMail.as_view(), name='create'),
]
from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from core.tasks import send_email_task
from .serializers import OTPSerializer

class SendRecoveryMail(CreateAPIView):
    '''email to recover user account'''
    def create(self, request, *args, **kwargs):
        subject = 'Test Email'
        message = 'This is a test email sent asynchronously via Celery.'
        recipient_list = ['singhshanu246@gmail.com']
        
        # Call the Celery task asynchronously
        send_email_task.delay(subject, message, recipient_list)
        # send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return Response({'status': 'Email sending in background.'})


class RequestOTP(CreateAPIView):
    '''request an OTP'''
    serializer_class = OTPSerializer
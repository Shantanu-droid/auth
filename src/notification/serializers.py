from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    '''serializer for the otp generation'''
    valid_until = serializers.DateTimeField(source='get_valid_until', read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = OTP
        fields = ['user', 'email', 'otp', 'valid_until']
        read_only_fields = ['otp', 'valid_until']
        extra_kwargs = dict(
            user={'write_only':True}
        )

    def validate(self, attrs):
        """
        Validate that the user with this email exists.
        """
        try:
            user = get_user_model().objects.get(email=attrs.get('email'))
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email address.")
        attrs['user'] = user
        return user
    
    def create(self, validated_data):
        return OTP.objects.create_otp(**validated_data)

    def get_valid_until(self, instance):
        '''get otp valid datetime'''
        return instance.created_at + \
            timedelta(minutes=settings.OTP_VALID_UNTIL_MINS)

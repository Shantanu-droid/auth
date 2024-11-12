import re

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = dict(
            password={'write_only':True, 'min_length':5}
        )

    def validate_password(self, value):
        '''validate password for its valid requirements'''
        password_requirements = {
            "requirements": [
                "At least one alphabetic character (a-z, A-Z)",
                "At least one numeric digit (0-9)",
                "At least one special character (e.g., !@#$%^&*(),.?\":{}|<>)",
                "No characters other than alphanumeric and the allowed special characters"
            ],
            "note": "Ensure your password is strong by following these guidelines to protect your account."
        }

        # Check if the string is a valid string
        if not re.fullmatch(r'[a-zA-Z0-9!@#$%^&*(),.?":{}|<>]*', value):
            raise ValidationError({'msg':'must contain only valid string literals'})
        # Check for at least one lowercase alphabetic character (a-z)
        has_lower_alphabet = re.search(r'[a-z]', value)

        # Check for at least one capital case al phabetic character (A-Z)
        has_higher_alphabet = re.search(r'[A-Z]', value)
    
        # Check for at least one numeric digit (0-9)
        has_digit = re.search(r'\d', value)

        # Check for at least one special character (non-alphanumeric)
        has_special_char = re.search(r'[!@#$%^&*(),.?":{}|<>]', value)

        if not (has_higher_alphabet and has_lower_alphabet and has_digit and has_special_char):
            raise ValidationError({'msg':password_requirements})
        
        return value
    
    def validate(self, attrs):
        username = attrs.get('name')
        email = attrs.get('email')
        password = attrs.get('password')

        username_set, password_set, email_set = set(username), set(password), set(email)

        if len(username_set & password_set) > settings.MIN_MATCH_PWD:
            raise ValidationError({'msg':'User name and password are too similar'})
        
        if len(email_set & password_set) > settings.MIN_MATCH_PWD:
            raise ValidationError({'msg':'Email and password are too similar'})

        return attrs

    def create(self, validated_data):
        '''create and return a user with encrypted password'''
        return get_user_model().objects.create_user(**validated_data)
from rest_framework import generics
from user.serializers.user import UserSerializer

class CreateUserView(generics.CreateAPIView):
    '''create a new user in the system'''
    serializer_class = UserSerializer
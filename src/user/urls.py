'''
URL mappings for the user APIs
'''

from django.urls import path
from user.views import user_views

app_name = 'user'

urlpatterns = [
    path('create/', user_views.CreateUserView.as_view(), name='create'),
]
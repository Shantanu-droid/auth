'''
URL mappings for the user APIs
'''
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.urls import path
from user.views import user_views
from user.views.password import LoginVeiw, LogoutView


app_name = 'user'

urlpatterns = [
    path('create/', user_views.CreateUserView.as_view(), name='create'),

    # rest jwt views
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', LoginVeiw.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
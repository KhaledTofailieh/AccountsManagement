from django.urls import path
from .views import SignUpView, authenticate_user

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('authenticate/', authenticate_user, name='authenticate')
]

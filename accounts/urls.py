from django.urls import path
from .views import UserLoginView, SignupView

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]

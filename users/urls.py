from django.urls import path
from .views import RegisterView, UserLoginView, ProfileUpdateView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]


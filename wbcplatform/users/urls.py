from django.conf.urls import include, url
from .views import register, activate, ProfileView
from django.contrib.auth import views
from .forms import UserLoginForm
from django.urls import path

urlpatterns = [
    url('accounts/login', views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=UserLoginForm
    ), name='login'),
    path('activate/<uidb64>/<token>/',
        activate, name='activate'),
    path('accounts/profile/', ProfileView.as_view(), name="profile"),
    url('accounts/', include("django.contrib.auth.urls")),
    url('oauth/', include("social_django.urls")),
    url('register/', register, name="register"),
]

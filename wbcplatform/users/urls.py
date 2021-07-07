from django.conf.urls import include, url
from users.views import dashboard, register, activate
from django.contrib.auth import views
from users.forms import UserLoginForm
from django.urls import path

urlpatterns = [
    url('accounts/login', views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=UserLoginForm
    ), name='login'),
    path('activate/<uidb64>/<token>/',
        activate, name='activate'),
    url('accounts/', include("django.contrib.auth.urls")),
    url('dashboard/', dashboard, name="dashboard"),
    url('oauth/', include("social_django.urls")),
    url('register/', register, name="register"),
]
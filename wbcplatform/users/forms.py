from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

# new user creation
class NewUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'New Password',
            'style': "margin-top:3px",
        }),
    )
    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control',
            'placeholder': 'Repeat Password',
            'style': "margin-top:3px",
        }),
        strip=False,
    )

    username = forms.CharField(
        label=(""),
        max_length=100,
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    email = forms.EmailField(
        label=(""),
        max_length=200,
        widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'style': "margin-top:3px"})
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

# user login
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email / Username'}
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

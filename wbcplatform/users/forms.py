from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Profile

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



# profile form
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    """
    From validation error
    If any error happened in the form, this function returns the error message
    :param form:
    :return:
    """
    msg=""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg
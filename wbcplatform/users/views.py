from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from .forms import NewUserCreationForm, UserLoginForm
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User

def dashboard(request):
    return render(request, "users/dashboard.html")

# user registration view
def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": NewUserCreationForm}
        )
    elif request.method == "POST":
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # reset to inactive until email is confirmed
            user.is_active = False
            user.backend = "users.backends.EmailUserNameBackend"
            user.save()
            current_site = get_current_site(request)

            # set up activation email
            mail_subject = 'Activate your WBC account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(mail_subject, message)

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()

            return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        # NEED TO FIGURE OUT User.DoesNotExist !!!
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.backend = "users.backends.EmailUserNameBackend"
        user.save()
        login(request, user)
        # return redirect("dashboard")
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid!')

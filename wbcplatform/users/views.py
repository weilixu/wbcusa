from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.urls import reverse
from users.forms import NewUserCreationForm

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
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("dashboard"))

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, CreateChannelForm
from django.contrib.auth.decorators import login_required
from .models import *


def landing_page(request):
    return render(request, "landing_page.html")


def register(request):
    form = SignUpForm()  # Initialize the form

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to the dashboard after successful registration
            return redirect("dashboard")

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to the dashboard after successful login
                return redirect("dashboard")
            else:
                # Handle invalid login credentials
                messages.info(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required(login_url=login_view)
def dashboard(request):
    user_authenticated = request.user.is_authenticated

    if user_authenticated:
        user_group = request.user.groups.first()

        if user_group:
            if user_group.name == "User":
                # Redirect students to student.html
                return render(
                    request, "dash.html", {"user_authenticated": user_authenticated}
                )
            elif user_group.name == "Admin":
                # For teachers, show the regular dashboard with assignment creation form
                return render(
                    request, "dash.html", {"user_authenticated": user_authenticated}
                )

        # For other groups or no group specified, show the regular dashboard
        return render(request, "dash.html", {"user_authenticated": user_authenticated})
    else:
        return render(request, "login.html")  # Redirect to login if not authenticated


def logout_view(request):
    logout(request)
    return redirect(register)  # Redirect to the registration page after logout


def create_channel(request):
    if request.method == "POST":
        form = CreateChannelForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            name = form.cleaned_data["Name"]
            description = form.cleaned_data["Description"]
            owner = CustomUser.objects.get(username=request.user.username)
            Channel.objects.create(name=name, description=description, creator=owner)
            return redirect(dashboard)
    else:
        form = CreateChannelForm()
        context = {"form": form}

    return render(request, "create_channel.html", context)

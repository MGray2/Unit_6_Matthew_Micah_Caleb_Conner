from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to different pages based on the selected group
            if user.groups.filter(name="Admin").exists():
                return redirect("dashboard")  # Redirect teachers to the dashboard
            elif user.groups.filter(name="User").exists():
                return redirect("student")  # Redirect students to the student page
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})


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
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def dashboard(request):
    user_authenticated = request.user.is_authenticated

    if user_authenticated:
        user_group = request.user.groups.first()

        if user_group:
            if user_group.name == "User":
                # Redirect students to student.html
                return render(
                    request, "student.html", {"user_authenticated": user_authenticated}
                )
            elif user_group.name == "Admin":
                # For teachers, show the regular dashboard with assignment creation form
                return render(
                    request,
                    "dashboard.html",
                    {"user_authenticated": user_authenticated},
                )

        # For other groups or no group specified, show the regular dashboard
        return render(
            request, "dashboard.html", {"user_authenticated": user_authenticated}
        )
    else:
        return render(request, "login.html")  # Redirect to login if not authenticated


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to the login page after logout

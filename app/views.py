# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to the dashboard after successful signup
            return redirect("dashboard")
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

    return render(request, "signin.html", {"form": form})

def dashboard(request):
    user_authenticated = request.user.is_authenticated

    if user_authenticated:
        user_group = request.user.groups.first()

        if user_group:
            if user_group.name == "User":
                # Redirect students to student.html
                return render(request, "dash.html", {"user_authenticated": user_authenticated})
            elif user_group.name == "Admin":
                # For teachers, show the regular dashboard with assignment creation form
                return render(request, "dash.html", {"user_authenticated": user_authenticated})

        # For other groups or no group specified, show the regular dashboard
        return render(request, "dash.html", {"user_authenticated": user_authenticated})
    else:
        return render(request, "signup.html")  # Redirect to login if not authenticated

def logout_view(request):
    logout(request)
    return redirect("signup")  # Redirect to the login page after logout

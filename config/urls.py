from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),  # Add this line for the admin page
    path("", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
]

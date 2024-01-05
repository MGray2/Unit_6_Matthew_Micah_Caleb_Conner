from django.contrib import admin
from django.urls import path
from app.views import register, login_view, logout_view, dashboard

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin page
    path("", register, name="register"),  # Registration page
    path("login/", login_view, name="login"),  # Login page
    path("logout/", logout_view, name="logout"),  # Logout page
    path("dashboard/", dashboard, name="dashboard"),  # Dashboard page
]

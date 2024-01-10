from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin page
    path("register/", register, name="register"),  # Registration page
    path("login/", login_view, name="login"),  # Login page
    path("logout/", logout_view, name="logout"),  # Logout page
    path("dashboard/", dashboard, name="dashboard"),  # Dashboard page
    path("create_channel/", create_channel, name="create_channel"),
    path("about/", about, name="about"),  # About page
    path("contact/", contact, name="contact"),  # Contact page
    path("channels/<str:channel_name>/", channel_view, name="channels"),
    path("channels/settings/<str:channel_name>/", channel_settings, name="settings"),
    path("profile/", profile, name="profile"), # Profile page
    path("", landing_page, name="landing_page"),  # landing page
]

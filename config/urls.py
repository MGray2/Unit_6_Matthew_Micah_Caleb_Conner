from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

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
    path("profile/", profile, name="profile"),  # Profile page
    path("delete_acount/", delete_account, name="delete_account"),  # account deletion
    path("", landing_page, name="landing_page"),  # landing page
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

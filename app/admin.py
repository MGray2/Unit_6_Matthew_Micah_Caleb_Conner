from django.contrib import admin
from .models import Channel, Comment, CustomUser, Membership

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Channel)
admin.site.register(Membership)

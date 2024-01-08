from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(models.Model):
    profile_picture = models.ImageField(
        upload_to=None, height_field=None, width_field=None, max_length=None
    )

    def __str__(self):
        return f"Name: {self.username}, Email: {self.email}, Password: {self.password}"


class Channel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_members = models.ManyToManyField(
        CustomUser, related_name="channels", through="Membership"
    )

    def __str__(self):
        return f"Name: {self.name}, Creator: {self.creator}, Chat Members: {self.chat_members}"


class Membership(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Member: {self.member.username} in Channel: {self.channel.name}"


class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"Comment by {self.owner.username} in {self.channel.name}"

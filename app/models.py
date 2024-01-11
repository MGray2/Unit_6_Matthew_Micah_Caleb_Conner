from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Username: {self.username}, Email: {self.email}"

    groups = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        related_name="customuser_set",
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        related_name="customuser_set",
        related_query_name="user",
    )


class Channel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat_members = models.ManyToManyField(
        CustomUser, related_name="channels", through="Membership"
    )
    MODE = (("Enabled", "Enabled"), ("Disabled", "Disabled"))
    safe_mode = models.CharField(
        max_length=10,
        choices=MODE,
    )

    def __str__(self):
        return f"Name: {self.name}, Creator: {self.creator}"


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

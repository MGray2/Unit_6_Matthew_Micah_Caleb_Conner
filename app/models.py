from django.db import models
from django.contrib.auth.models import User, Group


class Member(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"Name: {self.username}, Email: {self.email}, Password: {self.password}"


class Channel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(Member, on_delete=models.CASCADE)
    chat_members = models.ManyToManyField(
        Member, related_name="channels", through="Membership"
    )

    def __str__(self):
        return f"Name: {self.name}, Creator: {self.creator}, Chat Members: {self.chat_members}"


class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Member: {self.member.username} in Channel: {self.channel.name}"


class Comment(models.Model):
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"Comment by {self.owner.username} in {self.channel.name}"

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
from better_profanity import profanity


def landing_page(request):
    return render(request, "landing_page.html")


def register(request):
    form = SignUpForm()  # Initialize the form

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to the dashboard after successful registration
            return redirect("dashboard")

    return render(request, "register.html", {"form": form})


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
                messages.info(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@login_required(login_url=login_view)
def dashboard(request):
    user_authenticated = request.user.is_authenticated

    if user_authenticated:
        user_group = request.user.groups.first()

        if user_group:
            if user_group.name == "User":
                you = CustomUser.objects.get(username=request.user.username)
                channel_list = Channel.objects.filter(creator=you)
                involved_channels = Channel.objects.filter(chat_members=you).exclude(
                    creator=you
                )

                return render(
                    request,
                    "dash.html",
                    {
                        "user_authenticated": user_authenticated,
                        "channels": channel_list,
                        "involved_channels": involved_channels,
                    },
                )
            elif user_group.name == "Admin":
                you = CustomUser.objects.get(username=request.user.username)
                channel_list = Channel.objects.filter(creator=you)
                involved_channels = Channel.objects.filter(chat_members=you).exclude(
                    creator=you
                )

                return render(
                    request,
                    "dash.html",
                    {
                        "user_authenticated": user_authenticated,
                        "channels": channel_list,
                        "involved_channels": involved_channels,
                    },
                )

        # For other groups or no group specified, show the regular dashboard
        return render(request, "dash.html", {"user_authenticated": user_authenticated})
    else:
        return render(request, "login.html")  # Redirect to login if not authenticated


# logging in is not required
def logout_view(request):
    logout(request)
    return redirect(landing_page)  # Redirect to the registration page after logout


@login_required(login_url=login_view)
def create_channel(request):
    owner = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        form = CreateChannelForm(request.POST)
        if form.is_valid():
            channel_name = form.cleaned_data["Name"]
            description = form.cleaned_data["Description"]
            # stops you from making a channel with the same name
            if Channel.objects.filter(name=channel_name).exists():
                ...
            else:
                Channel.objects.create(
                    name=channel_name,
                    description=description,
                    creator=owner,
                )

    else:
        form = CreateChannelForm()

    context = {"form": form}
    return render(request, "create_channel.html", context)


# About Page
@login_required(login_url=login_view)
def about(request):
    return render(request, "about.html")


# Contact Page
@login_required(login_url=login_view)
def contact(request):
    return render(request, "contact.html")


@login_required(login_url=login_view)
def channel_view(request, channel_name):
    try:
        you = CustomUser.objects.get(username=request.user.username)
        channel_list = Channel.objects.filter(creator=you)
        involved_channels = Channel.objects.filter(chat_members=you).exclude(creator=you)
        C_List = set()
        for c1 in channel_list:
            C_List.add(c1)
        for c2 in involved_channels:
            C_List.add(c2)


        channel = Channel.objects.get(name=channel_name)
        channel_comments = Comment.objects.filter(channel=channel)
        you = CustomUser.objects.get(username=request.user.username)
        your_comments = Comment.objects.filter(owner=you, channel=channel)
        people_in_channel = channel.chat_members.exclude(id=channel.creator.id)
        context = {
            "channel": channel,
            "members": people_in_channel,
            "owner": channel.creator.username,
            "comments": channel_comments,
            "your_comments": your_comments,
            "all_in":C_List,
        }
        if request.method == "POST":
            text = request.POST.get("comment_text")
            # adding comments
            if text:
                if channel.safe_mode == "Enabled":
                    text = profanity.censor(text)
                Comment.objects.create(owner=you, channel=channel, message=text)
                # removing comments
            comment_id = request.POST.get("comment_remove")
            if comment_id:
                comment_to_rm = Comment.objects.get(
                    id=comment_id, owner=you, channel=channel
                )
                comment_to_rm.delete()
    except:
        return redirect(dashboard)
    return render(request, "channel.html", context)


@login_required(login_url=login_view)
def channel_settings(request, channel_name):
    channel = Channel.objects.get(name=channel_name)
    not_channel_members = CustomUser.objects.exclude(
        channels=channel
    )  # People Not In Channel
    channel_members = channel.chat_members.exclude(id=channel.creator.id)
    if request.method == "POST":
        form = UpdateChannelForm(request.POST)
        if form.is_valid():
            # Form Variables
            new_name = form.cleaned_data["Name"]
            new_desc = form.cleaned_data["Description"]
            new_mode = form.cleaned_data["SafeMode"]
            person_to_add = request.POST.get("selected_person")
            person_to_remove = request.POST.get("person_to_remove")
            # If New Channel Name
            if new_name:
                channel.name = new_name
                channel.save()
                # If New Description
            if new_desc:
                channel.description = new_desc
                channel.save()
            if new_mode:
                channel.safe_mode = new_mode
                channel.save()
                # Add Member To Channel
            if person_to_add:
                selected_person = CustomUser.objects.get(username=person_to_add)
                Membership.objects.create(member=selected_person, channel=channel)
                # Delete Member To Channel
            if person_to_remove:
                selected_person = CustomUser.objects.get(username=person_to_remove)
                to_remove = Membership.objects.get(
                    member=selected_person, channel=channel
                )
                to_remove.delete()

        return redirect(reverse(channel_view, args=[channel_name]))

    else:
        form = UpdateChannelForm()
    context = {
        "channel": channel,
        "form": form,
        "people_add": not_channel_members,
        "people_rm": channel_members,
    }
    return render(request, "channel_settings.html", context)


@login_required(login_url=login_view)
def profile(request):
    user = request.user
    channels = user.channels.all()

    if request.method == "POST":
        combined_form = CombinedProfileForm(request.POST, request.FILES, instance=user)

        if combined_form.is_valid():
            combined_form.save()
            return redirect("profile")

    else:
        combined_form = CombinedProfileForm(instance=user)

    context = {
        "user": user,
        "channels": channels,
        "combined_form": combined_form,
    }
    return render(request, "profile.html", context)


def delete_account(request):
    delete_confirm = request.POST.get("d")
    if delete_confirm == "Confirm Delete Account":
        target = CustomUser.objects.get(id=request.user.id)
        logout(request)
        target.delete()
        return redirect(landing_page)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import PassengerRegistrationForm


def register(request):
    if request.method == "POST":
        form = PassengerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully. Please log in."
            )
            return redirect("accounts:login")

    else:
        form = PassengerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")

            # Temporarily stay on login until the dashboard exists
            return render(request, "accounts/login.html")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully."
    )
    return redirect("accounts:login")
from django.shortcuts import render, redirect

from .forms import PassengerRegistrationForm


def register(request):
    if request.method == "POST":
        form = PassengerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = PassengerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})
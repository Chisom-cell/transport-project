from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PassengerRegistrationForm
from .services import verify_identity_numbers


def register(request):
    if request.method == 'POST':
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            success, message = verify_identity_numbers(
                nin=user.nin,
                abssin=user.abssin,
                first_name=user.first_name,
                last_name=user.last_name
            )

            if success:
                user.is_verified = True
                user.save()
                messages.success(request, "Account created and verified successfully!")
                return redirect('login')
            else:
                messages.error(request, f"Verification failed: {message}")
    else:
        form = PassengerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


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
            return redirect("accounts:profile")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "accounts/login.html")

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"user": request.user})


def user_logout(request):
    logout(request)
    messages.success(
        request,
        "You have been logged out successfully."
    )
    return redirect("accounts:login")



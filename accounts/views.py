from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PassengerRegistrationForm
from .services import verify_identity_numbers
from .forms import IdentityVerificationForm
from .services import verify_identity_numbers

from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(
                request,
                "Account created successfully! You can verify your NIN and "
                "ABSSIN anytime from your profile."
            )
            return redirect('accounts:profile')
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




@login_required
def verify_identity(request):
    if request.user.is_verified:
        messages.info(request, "Your account is already verified.")
        return redirect("accounts:profile")

    if request.method == "POST":
        form = IdentityVerificationForm(request.POST)
        if form.is_valid():
            nin = form.cleaned_data["nin"]
            abssin = form.cleaned_data["abssin"]

            success, message = verify_identity_numbers(
                nin=nin,
                abssin=abssin,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
            )

            if success:
                request.user.nin = nin
                request.user.abssin = abssin
                request.user.is_verified = True
                request.user.save()
                messages.success(request, "Identity verified successfully.")
                return redirect("accounts:profile")

            messages.error(request, f"Verification failed: {message}")
    else:
        form = IdentityVerificationForm()

    return render(request, "accounts/verify_identity.html", {"form": form})
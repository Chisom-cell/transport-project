from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from bookings.models import Booking

from .forms import PassengerRegistrationForm, IdentityVerificationForm
from .services import verify_identity_numbers


def register(request):
    """Registers a new user and redirects them to the login page."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')  # Changed from accounts:profile

    if request.method == 'POST':
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! Please log in to access your dashboard."
            )
            return redirect('accounts:login')
    else:
        form = PassengerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """Log in a user and redirect according to their role."""

    if request.user.is_authenticated:

        if request.user.role in [
            request.user.Role.SUPER_ADMIN,
            request.user.Role.GOVERNMENT_ADMIN,
        ]:
            return redirect("analytics:dashboard")

        return redirect("accounts:dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            # -----------------------------
            # ROLE-BASED REDIRECT
            # -----------------------------

            if user.role in [
                user.Role.SUPER_ADMIN,
                user.Role.GOVERNMENT_ADMIN,
            ]:
                return redirect(
                    "analytics:dashboard"
                )

            return redirect(
                "accounts:dashboard"
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


@login_required
def dashboard(request):
    user = request.user

    if user.role == user.Role.SUPER_ADMIN:
        return render(request, "dashboards/super_admin.html")

    elif user.role == user.Role.GOVERNMENT_ADMIN:
        return render(request, "dashboards/government_admin.html")

    elif user.role == user.Role.OPERATOR_ADMIN:
        return render(request, "dashboards/operator_admin.html")

    elif user.role == user.Role.DRIVER:
        return render(request, "dashboards/driver.html")

    # -----------------------------------------
    # PASSENGER DASHBOARD
    # -----------------------------------------

    recent_bookings = (
        Booking.objects
        .filter(passenger=user)
        .select_related("trip")
        .order_by("-created_at")[:5]
    )

    upcoming_trip = (
        Booking.objects
        .filter(
            passenger=user,
            status="CONFIRMED"
        )
        .select_related("trip")
        .order_by("created_at")
        .first()
    )

    return render(
        request,
        "dashboards/passenger.html",
        {
            "recent_bookings": recent_bookings,
            "upcoming_trip": upcoming_trip,
        }
    )




@login_required
def profile(request):
    """Displays the authenticated user's profile page."""
    return render(request, "accounts/profile.html", {"user": request.user})


def user_logout(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")


@login_required
def verify_identity(request):
    """Allows passengers to verify their NIN and ABSSIN."""
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
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from bookings.models import Booking

from .forms import (
    IdentityVerificationForm,
    PassengerRegistrationForm,
)
from .services import verify_identity_numbers


# =========================================================
# REGISTER
# =========================================================

def register(request):
    """Register a new passenger account."""

    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = PassengerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                (
                    "Account created successfully! "
                    "Please log in to access your dashboard."
                ),
            )

            return redirect("accounts:login")

    else:
        form = PassengerRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):
    """Log in a user and redirect according to their role."""

    if request.user.is_authenticated:
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

            if not user.is_active:
                messages.error(
                    request,
                    "Your account is inactive. Please contact an administrator.",
                )
                return render(
                    request,
                    "accounts/login.html",
                )

            login(request, user)

            messages.success(
                request,
                "Login successful.",
            )

            return redirect("accounts:dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    user = request.user

    # -----------------------------------------------------
    # SUPER ADMIN
    # -----------------------------------------------------

    if user.role == user.Role.SUPER_ADMIN:
        return render(
            request,
            "dashboards/super_admin.html",
        )

    # -----------------------------------------------------
    # GOVERNMENT ADMIN
    # -----------------------------------------------------

    if user.role == user.Role.GOVERNMENT_ADMIN:
        return render(
            request,
            "dashboards/government_admin.html",
        )

    # -----------------------------------------------------
    # OPERATOR ADMIN
    # -----------------------------------------------------

    if user.role == user.Role.OPERATOR_ADMIN:
        return render(
            request,
            "dashboards/operator_admin.html",
        )

    # -----------------------------------------------------
    # DRIVER
    # -----------------------------------------------------

    if user.role == user.Role.DRIVER:
        return render(
            request,
            "dashboards/driver.html",
        )

    # -----------------------------------------------------
    # PASSENGER
    # -----------------------------------------------------

    recent_bookings = (
        Booking.objects
        .filter(
            passenger=user,
        )
        .select_related(
            "trip",
            "trip__route",
            "trip__vehicle",
        )
        .order_by("-created_at")[:5]
    )

    upcoming_trip = (
        Booking.objects
        .filter(
            passenger=user,
            status=Booking.Status.CONFIRMED,
            trip__departure_time__gte=timezone.now(),
        )
        .select_related(
            "trip",
            "trip__route",
            "trip__vehicle",
        )
        .order_by("trip__departure_time")
        .first()
    )

    return render(
        request,
        "dashboards/passenger.html",
        {
            "recent_bookings": recent_bookings,
            "upcoming_trip": upcoming_trip,
        },
    )


# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):
    """Display the authenticated user's profile."""

    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user,
        },
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def user_logout(request):
    """Log out the current user."""

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully.",
    )

    return redirect("accounts:login")


# =========================================================
# IDENTITY VERIFICATION
# =========================================================

@login_required
def verify_identity(request):
    """Allow passengers to verify their NIN and ABSSIN."""

    if request.user.is_verified:
        messages.info(
            request,
            "Your account is already verified.",
        )

        return redirect(
            "accounts:profile"
        )

    if request.method == "POST":

        form = IdentityVerificationForm(
            request.POST
        )

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

                request.user.save(
                    update_fields=[
                        "nin",
                        "abssin",
                        "is_verified",
                    ]
                )

                messages.success(
                    request,
                    "Identity verified successfully.",
                )

                return redirect(
                    "accounts:profile"
                )

            messages.error(
                request,
                f"Verification failed: {message}",
            )

    else:
        form = IdentityVerificationForm()

    return render(
        request,
        "accounts/verify_identity.html",
        {
            "form": form,
        },
    )
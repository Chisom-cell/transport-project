from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login


def role_required(*roles):
    """
    Restrict a view to specific user roles.

    Super Admin has system-wide access.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            # Super Admin has system-wide access
            if request.user.role == request.user.Role.SUPER_ADMIN:
                return view_func(request, *args, **kwargs)

            # Check whether user's role is allowed
            if request.user.role not in roles:
                messages.error(
                    request,
                    "You do not have permission to access this page.",
                )
                return redirect("accounts:dashboard")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
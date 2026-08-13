from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # Main transport pages
    path("", include("transport.urls")),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Bookings
    path("bookings/", include("bookings.urls")),

    # Notifications
    path("notifications/", include("notifications.urls")),

    # Complaints
    path("complaints/", include("complaints.urls")),
]
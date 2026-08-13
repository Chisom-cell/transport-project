from .models import Notification


def create_notification(
    user,
    title,
    message,
    notification_type,
):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )


def booking_confirmed(user, booking):
    return create_notification(
        user=user,
        title="Booking Confirmed",
        message=(
            f"Your booking {booking.reference} "
            f"has been confirmed."
        ),
        notification_type=Notification.NotificationType.BOOKING_CONFIRMED,
    )


def booking_cancelled(user, booking):
    return create_notification(
        user=user,
        title="Booking Cancelled",
        message=(
            f"Your booking {booking.reference} "
            f"has been cancelled."
        ),
        notification_type=Notification.NotificationType.BOOKING_CANCELLED,
    )
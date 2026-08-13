from django.urls import path
from . import views

app_name = "tracking"

urlpatterns = [
    path("", views.trip_list, name="list"),
    path("<int:trip_id>/", views.trip_detail, name="detail"),
]

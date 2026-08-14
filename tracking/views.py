from django.shortcuts import render, get_object_or_404

from transport.models import Trip


def trip_list(request):
	trips = Trip.objects.filter(status__in=[
		Trip.Status.SCHEDULED,
		Trip.Status.BOARDING,
		Trip.Status.IN_TRANSIT,
	])
	return render(request, "tracking/tracking_list.html", {"trips": trips})


def trip_detail(request, trip_id):
	trip = get_object_or_404(Trip, pk=trip_id)
	return render(request, "tracking/tracking_detail.html", {"trip": trip})

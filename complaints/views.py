from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ComplaintForm
from .models import Complaint


@login_required
def create_complaint(request):

    if request.method == "POST":

        form = ComplaintForm(request.POST)

        if form.is_valid():

            complaint = form.save(commit=False)

            complaint.passenger = request.user

            complaint.save()

            return redirect("complaints:list")

    else:

        form = ComplaintForm()

    return render(
        request,
        "complaints/create_complaint.html",
        {
            "form": form,
        },
    )


@login_required
def complaint_list(request):

    complaints = Complaint.objects.filter(
        passenger=request.user
    ).order_by("-created_at")

    return render(
        request,
        "complaints/complaint_list.html",
        {
            "complaints": complaints,
        },
    )
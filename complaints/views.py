from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ComplaintForm


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
        {"form": form}
    )
def complaint_list(request):
    return render(request, 'complaints/complaint_list.html')
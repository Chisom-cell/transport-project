from django.urls import path

from . import views


app_name = "complaints"


urlpatterns = [

    path(
        "",
        views.complaint_list,
        name="list",
    ),

    path(
        "create/",
        views.create_complaint,
        name="create",
    ),
    
]
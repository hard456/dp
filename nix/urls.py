from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.testik, name="testik"),
    path("upload/", views.upload_experiment, name="upload"),
    path("experiment/<slug:id>/file", views.show_file),
]

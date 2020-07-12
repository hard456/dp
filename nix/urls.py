from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_home_page, name="home_page"),
    path("test/", views.testik, name="testik"),
    path("upload/", views.upload_experiment, name="upload_experiment"),
    path("experiment/<slug:id>/files", views.show_experiment_page, name="experiment"),
    path("experiment/<slug:id>/upload", views.upload_files, name="upload_files"),
    path("experiment/<slug:id>/download/<str:name>", views.download_file, name="download"),
    path("experiment/<slug:id>/delete/<str:name>", views.delete_file, name="delete"),
    path("experiment/<slug:id>/metadata", views.show_metadata_page, name="metadata"),
    path("experiment/<slug:id>/metadata/show", views.show_metadata, name="show_metadata"),
    path("experiment/<slug:id>/find", views.show_find_page, name="find"),
    path("experiment/<slug:id>/query", views.process_query, name="query"),
    path("experiment/<slug:id>/signal", views.show_signal_page, name="signal"),
]

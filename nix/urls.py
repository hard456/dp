from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.testik, name="testik"),
    path("upload/", views.upload_experiment, name="upload"),
    path("experiment/<slug:id>/experiment", views.show_experiment, name="experiment"),
    path("experiment/<slug:id>/experiment/download", views.download_experiment, name="download_experiment"),
    path("experiment/<slug:id>/json-ld", views.show_json_ld, name="json-ld"),
    path("experiment/<slug:id>/json-ld/convert", views.convert_experiment, name="convert_experiment"),
    path("experiment/<slug:id>/json-ld/download", views.download_json_ld, name="download_json_ld"),
    path("experiment/<slug:id>/sparql", views.show_sparql, name="sparql"),
    path("experiment/<slug:id>/query", views.process_query, name="query"),
    path("experiment/<slug:id>/graph", views.show_graph, name="graph"),
]

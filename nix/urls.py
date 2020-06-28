from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.testik, name="testik"),
    path("upload/", views.upload_experiment, name="upload"),
    path("experiment/<slug:id>/file", views.show_file, name="experiment"),
    path("experiment/<slug:id>/json-ld", views.show_json_ld, name="json-ld"),
    path("experiment/<slug:id>/sparql", views.show_sparql, name="sparql"),
    path("experiment/<slug:id>/query", views.process_query, name="query"),
    path("experiment/<slug:id>/graph", views.show_graph, name="graph"),
]

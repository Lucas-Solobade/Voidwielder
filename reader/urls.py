from django.urls import path

from . import views

app_name = "reader"

urlpatterns = [
    path("", views.home, name="home"),
    path("arcos/<slug:arc_slug>/", views.arc_detail, name="arc"),
    path("ler/arco/<slug:arc_slug>/", views.read_arc, name="read_arc"),
    path("ler/<slug:arc_slug>/<int:page>/", views.read_page, name="read"),
    path("buscar/", views.search, name="search"),
    path("estudos/", views.studies, name="studies"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]

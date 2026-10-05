from django.urls import path

from . import views

app_name = "reader"

urlpatterns = [
    path("", views.home, name="home"),
    path("hqs/homus-bananus/", views.hq_detail, name="hq"),
    path("arcos/<slug:arc_slug>/", views.arc_detail, name="arc"),
    path("ler/arco/<slug:arc_slug>/", views.read_arc, name="read_arc"),
    path("ler/<slug:arc_slug>/<int:page>/", views.read_page, name="read"),
    path("buscar/", views.search, name="search"),
    path("estudos/", views.studies, name="studies"),
    path("jogos/pipo-e-o-correio-das-estrelas/", views.game, name="game"),
    path("playground/", views.playground, name="playground"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]

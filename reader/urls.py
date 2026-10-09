from django.urls import path

from . import views

app_name = "reader"

urlpatterns = [
    path("", views.home, name="home"),
    path("hqs/homus-bananus/", views.hq_detail, name="hq"),
    path("hqs/homus-bananus/extras/", views.hq_extras, name="hq_extras"),
    path("arcos/<slug:arc_slug>/", views.arc_detail, name="arc"),
    path("ler/arco/<slug:arc_slug>/", views.read_arc, name="read_arc"),
    path("ler/<slug:arc_slug>/<int:page>/", views.read_page, name="read"),
    path("buscar/", views.search, name="search"),
    path("livros/a-casa-das-medidas/", views.book_detail, name="book_detail"),
    path("livros/a-casa-das-medidas/ler/<int:page>/", views.read_book, name="read_book"),
    path("livros/linux-do-zero-ao-avancado/", views.linux_detail, name="linux_detail"),
    path("livros/linux-do-zero-ao-avancado/ler/<int:page>/", views.read_linux, name="read_linux"),
    path("livros/python-do-zero-ao-avancado/", views.python_detail, name="python_detail"),
    path("livros/python-do-zero-ao-avancado/ler/<int:page>/", views.read_python, name="read_python"),
    path("livros/desenvolvimento-web-do-zero-ao-avancado/", views.web_detail, name="web_detail"),
    path("livros/desenvolvimento-web-do-zero-ao-avancado/ler/<int:page>/", views.read_web, name="read_web"),
    path("estudos/", views.studies, name="studies"),
    path("estudos/logica-de-programacao-e-algoritmos/", views.study_guide, name="study_guide"),
    path("jogos/pipo-e-o-correio-das-estrelas/", views.game, name="game"),
    path("jogos/mila-e-o-jardim-das-nuvens/", views.garden_game, name="garden_game"),
    path("jogos/lilo-e-o-festival-das-bolhas/", views.bubble_game, name="bubble_game"),
    path("playground/", views.playground, name="playground"),
    path("robots.txt", views.robots, name="robots"),
    path("sitemap.xml", views.sitemap, name="sitemap"),
]

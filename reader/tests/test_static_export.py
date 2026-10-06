from unittest.mock import Mock

from django.test import Client

from scripts import export_static


def test_github_pages_export_uses_repository_path(monkeypatch):
    destination = Mock()
    monkeypatch.setattr(export_static, "destination_for", lambda _: destination)
    monkeypatch.setattr(export_static, "SITE_ORIGIN", "https://example.github.io/Voidwielder")
    monkeypatch.setattr(export_static, "SITE_BASE_PATH", "/Voidwielder")

    export_static.write_page(Client(), "/")
    html = destination.write_text.call_args.args[0]

    assert 'data-site-base="/Voidwielder"' in html
    assert 'href="/Voidwielder/buscar/"' in html
    assert 'href="/Voidwielder/static/reader/css/site.css' in html
    assert 'href="https://example.github.io/Voidwielder/"' in html
    assert 'href="/buscar/"' not in html


def test_export_keeps_external_and_fragment_links(monkeypatch):
    monkeypatch.setattr(export_static, "SITE_BASE_PATH", "/Voidwielder")
    html = '<a href="/estudos/">Estudos</a><a href="#inicio">Início</a><a href="https://example.com/">Externo</a>'

    assert export_static.prefix_local_urls(html) == (
        '<a href="/Voidwielder/estudos/">Estudos</a>'
        '<a href="#inicio">Início</a>'
        '<a href="https://example.com/">Externo</a>'
    )

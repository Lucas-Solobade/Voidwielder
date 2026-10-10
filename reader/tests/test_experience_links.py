import re
from pathlib import Path


EXPERIENCES_DIR = Path(__file__).resolve().parents[2] / "experiencias"
ROOT_RELATIVE_URL = re.compile(r'\b(?:href|src|action)=["\']/[^/]')


def test_standalone_experiences_use_portable_internal_links():
    """Standalone pages must also work below a GitHub Pages repository path."""
    pages = sorted(EXPERIENCES_DIR.glob("*/index.html"))

    assert pages, "Nenhuma experiência independente encontrada."
    for page in pages:
        html = page.read_text(encoding="utf-8")
        assert not ROOT_RELATIVE_URL.search(html), (
            f"{page.relative_to(EXPERIENCES_DIR.parent)} usa uma URL absoluta da raiz. "
            "Use caminhos relativos para preservar o prefixo do GitHub Pages."
        )

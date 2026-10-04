from django.http import HttpRequest

from .catalog import ARCS, MANGA


def site_catalog(_: HttpRequest) -> dict[str, object]:
    """Make navigation metadata available without duplicating view logic."""
    return {"arcs": ARCS, "manga": MANGA}

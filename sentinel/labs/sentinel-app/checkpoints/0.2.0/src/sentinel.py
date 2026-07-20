#!/usr/bin/env python3
"""Point d'entrée stable de Sentinel 0.2.0.

La campagne 2 introduit plusieurs responsabilités. Le lanceur reste volontairement
court : le détail se trouve dans les modules voisins, que l'apprenant peut étudier
séparément.
"""

from cli import build_parser, main
from configuration import ConfigurationError, Settings, load_settings
from diagnostic import collect_status, render_status
from state import read_status, write_status
from version import VERSION


# Cette façade conserve les imports utilisés dans les premiers TP et leurs tests.
__all__ = [
    "VERSION",
    "ConfigurationError",
    "Settings",
    "build_parser",
    "collect_status",
    "load_settings",
    "main",
    "read_status",
    "render_status",
    "write_status",
]


if __name__ == "__main__":
    raise SystemExit(main())

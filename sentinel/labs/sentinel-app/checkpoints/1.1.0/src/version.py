"""Version et révision exposées aux outils de supervision en campagne 12."""

import os


VERSION = "1.1.0"
REVISION = os.environ.get("SENTINEL_REVISION", "unknown")

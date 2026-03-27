"""User-level config/data locations when installed from a wheel."""

from __future__ import annotations

import logging
from pathlib import Path

_logger = logging.getLogger(__name__)


def _maybe_migrate_legacy_user_dirs(home: Path) -> None:
    """If ~/.market-helm is missing, rename ~/.market-desk once."""
    dest = home / ".market-helm"
    if dest.exists():
        return
    md = home / ".market-desk"
    if not md.exists():
        return
    try:
        md.rename(dest)
        _logger.info("Migrated user config: ~/.market-desk -> ~/.market-helm")
    except OSError as e:
        _logger.warning("Could not migrate legacy user config dir: %s", e)


def user_config_dir() -> Path:
    """Directory for app config and data: ~/.market-helm when installed from a wheel.

    On first use, if that folder does not exist but ``~/.market-desk`` does, it is
    renamed to ``~/.market-helm`` automatically.
    """
    home = Path.home()
    _maybe_migrate_legacy_user_dirs(home)
    return home / ".market-helm"

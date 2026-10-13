"""Smoke tests del monorepo arduino-api-python.

Validan que ambos subproyectos importan su app sin errores y que la
estructura del repo es sana. No requiere hardware Arduino.
"""

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_readme_and_gitignore():
    assert (REPO / "README.md").exists()
    assert (REPO / ".gitignore").exists()


def test_temp_humedad_app_imports():
    appdir = REPO / "temp-humedad"
    sys.path.insert(0, str(appdir))
    try:
        mod = importlib.import_module("main")
        assert hasattr(mod, "app")
    finally:
        sys.path.pop(0)
        sys.modules.pop("main", None)


def test_distancia_app_imports():
    appdir = REPO / "distancia"
    sys.path.insert(0, str(appdir))
    try:
        mod = importlib.import_module("app")
        assert hasattr(mod, "app")
    finally:
        sys.path.pop(0)
        sys.modules.pop("app", None)


def test_no_venv_tracked():
    """Asegura que no haya un venv commiteado en git (sí puede existir en disco)."""
    import subprocess

    tracked = subprocess.run(
        ["git", "ls-files", ".env", ".venv", "venv"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert not tracked, f"Hay venv/env commiteado: {tracked}"

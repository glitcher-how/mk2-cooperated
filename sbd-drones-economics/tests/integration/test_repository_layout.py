"""Integration tests validating the repository layout essentials."""

from pathlib import Path


def test_required_directories_exist() -> None:
    """The top-level directories required by the specification must exist."""
    repo_root = Path(__file__).resolve().parents[2]
    for rel_path in [
        "docs",
        "components",
        "systems",
        "demos",
        "broker",
        "tests/e2e",
        "tests/integration",
    ]:
        assert (repo_root / rel_path).exists(), rel_path

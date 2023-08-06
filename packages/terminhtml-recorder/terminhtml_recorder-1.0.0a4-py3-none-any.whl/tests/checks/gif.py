from pathlib import Path


def assert_is_valid_gif(path: Path):
    """
    Check if the given path is a valid GIF.
    """
    with path.open("rb") as f:
        assert f.read(3) == b"GIF"
    assert path.exists()
    assert path.is_file()
    assert path.stat().st_size > 0

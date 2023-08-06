from pathlib import Path

import pytest

from terminhtml_recorder.temp_path import create_temp_path


@pytest.fixture
def temp_folder() -> Path:
    with create_temp_path() as temp_path:
        yield temp_path

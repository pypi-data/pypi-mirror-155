from pathlib import Path

from terminhtml_recorder.formats import OutputFormat
from terminhtml_recorder.temp_path import create_temp_path
from tests.checks.gif import assert_is_valid_gif
from tests.fixtures.temp_folder import temp_folder
from tests.generate import create_terminhtml_demo_gif


def test_recorder(temp_folder: Path):
    gif = create_terminhtml_demo_gif(temp_folder / "terminhtml-demo.gif")
    # TODO: Verify GIF output in tests
    assert gif.format == OutputFormat.GIF
    assert_is_valid_gif(gif.path)
    assert gif.path.parent == temp_folder

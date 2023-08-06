from terminhtml_recorder.formats import OutputFormat
from terminhtml_recorder.temp_path import create_temp_path
from tests.generate import create_terminhtml_demo_gif


def test_recorder():
    with create_temp_path() as temp_folder:
        gif = create_terminhtml_demo_gif(temp_folder / "terminhtml-demo.gif")
        # TODO: Verify GIF output in tests
        assert gif.format == OutputFormat.GIF
        assert gif.path.exists()
        assert gif.path.is_file()
        assert gif.path.stat().st_size > 0
        assert gif.path.parent == temp_folder

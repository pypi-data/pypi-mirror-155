"""
Run this script to generate the files in input_files so that
they can be manually QA'ed.
"""

from pathlib import Path

from terminhtml.main import TerminHTML

from terminhtml_recorder.formats import OutputFormat
from terminhtml_recorder.recorder import Recording, TerminHTMLRecorder
from tests.config import TERMINHTML_DEMO_GIF, TERMINHTML_DEMO_HTML


def create_terminhtml_demo_gif(out_path: Path = TERMINHTML_DEMO_GIF) -> Recording:
    term = TerminHTML.from_commands(
        ["python -m terminhtml.demo_output"],
        prompt_matchers=["\\[0m: "],
        input=["Nick DeRobertis"],
    )
    text = term.to_html()
    TERMINHTML_DEMO_HTML.write_text(text)
    recorder = TerminHTMLRecorder(text)
    recording = recorder.record(out_path, OutputFormat.GIF)
    return recording


if __name__ == "__main__":
    create_terminhtml_demo_gif()

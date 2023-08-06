import os
import sys
from pathlib import Path
from typing import Optional

import typer
from cliconf import CLIAppConfig, CLIConf, configure
from pyappconf import ConfigFormats

from terminhtml_recorder.exc import NoHTMLFoundException
from terminhtml_recorder.formats import OutputFormat
from terminhtml_recorder.recorder import (
    PageInteractor,
    TerminHTMLRecorder,
    default_page_interactor,
)

cli = CLIConf(
    name="terminhtml-recorder",
    help="Record TerminHTML animated output to a video file.",
)


@cli.command()
@configure(
    CLIAppConfig(
        app_name="terminhtml-recorder",
        config_name="terminrec",
        default_format=ConfigFormats.PY,
        py_config_imports=[
            "from pathlib import Path",
            "from terminhtml_recorder import PageLocators, default_page_interactor, OutputFormat",
            "import terminhtml_recorder.recorder",
            "from terminhtml_recorder.cli import record",
        ],
    )
)
def record(
    in_path: Optional[Path] = typer.Option(
        None,
        "--input-path",
        "-i",
        help="Path of file containing TerminHTML output. If not passed, must be piped to stdin.",
    ),
    out_path: Optional[Path] = typer.Option(
        None,
        "--output-path",
        "-o",
        help="Path of file to write recording to. Defaults to terminhtml.<output-format>",
        show_default=False,
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.GIF, "--format", "-f", help="Format of recording"
    ),
    delay: float = typer.Option(
        1.1,
        "--delay",
        "-d",
        help="Delay from browser start until recording start. Increase if you see an uninitialized terminal at the start. Decrease if you don't see the beginning of typing.",
    ),
    interactor: PageInteractor = default_page_interactor,
):
    """
    Record TerminHTML animated output to a video file.
    """
    if in_path is not None:
        html = in_path.read_text()
    # Else if input was piped to stdin
    elif not sys.stdin.isatty() and not os.getenv("PYCHARM_HOSTED"):
        # Read HTML from stdin
        html = sys.stdin.read()
    else:
        raise NoHTMLFoundException(
            f"No HTML passed. Must either specify an input file or pipe HTML to stdin."
        )

    if not html:
        raise NoHTMLFoundException(
            f"Empty HTML found. Must either specify a valid input file or pipe HTML to stdin."
        )

    out_path = out_path or Path("terminhtml").with_suffix(f".{output_format.value}")

    recorder = TerminHTMLRecorder(html, interactor)
    recorder.record(out_path, format=output_format, delay=delay)


if __name__ == "__main__":
    cli()

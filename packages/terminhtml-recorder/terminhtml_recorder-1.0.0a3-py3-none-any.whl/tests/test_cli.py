import shlex
from pathlib import Path
from typing import Sequence

from click.testing import Result
from cliconf import CLIConf
from cliconf.testing import CLIRunner

from terminhtml_recorder.cli import cli
from tests import ext_click
from tests.checks.gif import assert_is_valid_gif
from tests.config import TERMINHTML_DEMO_HTML
from tests.fixtures.temp_folder import temp_folder

runner = CLIRunner()


class CLIRunnerException(Exception):
    pass


def run(args: Sequence[str]) -> Result:
    result = runner.invoke(cli, args)
    if result.exit_code != 0:
        output = ext_click.result_to_message(result)
        command = shlex.join([cli.info.name, *args])
        raise CLIRunnerException(
            f"{command} with exited with code {result.exit_code}.\n{output}"
        )
    return result


def test_record_from_file(temp_folder: Path):
    out_path = temp_folder / "output.gif"
    run(["-i", str(TERMINHTML_DEMO_HTML), "-o", str(out_path)])
    assert_is_valid_gif(out_path)

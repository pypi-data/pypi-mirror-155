import shlex
from pathlib import Path
from typing import Sequence, Tuple

from click.testing import Result

from cliconf.main import CLIConf
from cliconf.testing import CLIRunner
from tests import ext_click
from tests.config import CONFIGS_DIR, PLAIN_CONFIGS_DIR
from tests.fixtures.cliconfs import (
    single_command_py_cliconf,
    single_command_py_cliconf_in_temp_dir,
    single_command_yaml_cliconf,
    single_command_yaml_cliconf_in_temp_dir,
)

runner = CLIRunner()


class CLIRunnerException(Exception):
    pass


def run(instance: CLIConf, args: Sequence[str]) -> Result:
    result = runner.invoke(instance, args)
    if result.exit_code != 0:
        output = ext_click.result_to_message(result)
        command = shlex.join([instance.info.name, *args])
        raise CLIRunnerException(
            f"{command} with exited with code {result.exit_code}.\n{output}"
        )
    return result


def test_single_command_cliconf_reads_from_yaml_config():
    result = run(single_command_yaml_cliconf, ["a", "2"])
    assert result.stdout == "a 2 45.6\n"


def test_single_command_cliconf_prints_help():
    result = run(single_command_yaml_cliconf, ["--help"])
    assert "A  [required]" in result.stdout
    assert "B  b help  [required]" in result.stdout
    assert "--c FLOAT" in result.stdout
    assert "c help  [default: 3.2]" in result.stdout
    assert "--help" in result.stdout


def test_single_command_cliconf_reads_py_config():
    result = run(single_command_py_cliconf, ["a", "2"])
    assert result.stdout == "a 2 123.4 custom 123.4\n"


def test_single_command_cliconf_reads_from_environment_over_config(monkeypatch):
    monkeypatch.setenv("MYAPP_C", "98.3")
    result = run(single_command_yaml_cliconf, ["a", "2"])
    assert result.stdout == "a 2 98.3\n"


def test_single_command_cliconf_writes_config_file_py(
    single_command_py_cliconf_in_temp_dir: Tuple[CLIConf, Path]
):
    cliconf_obj, temp_path = single_command_py_cliconf_in_temp_dir
    result = run(cliconf_obj, ["--config-gen"])
    assert "Saving config to" in result.stdout

    # Check that generated files are the same as in input_files
    for file_name in ("two.py", "two.pyi"):
        input_file = PLAIN_CONFIGS_DIR / file_name
        output_file = temp_path / file_name
        assert input_file.read_text() == output_file.read_text()


def test_single_command_cliconf_writes_config_file_yaml(
    single_command_yaml_cliconf_in_temp_dir: Tuple[CLIConf, Path]
):
    cliconf_obj, temp_path = single_command_yaml_cliconf_in_temp_dir
    result = run(cliconf_obj, ["--config-gen"])
    assert "Saving config to" in result.stdout

    # Check that generated files are the same as in input_files
    file_name = "one.yaml"
    input_file = PLAIN_CONFIGS_DIR / file_name
    output_file = temp_path / file_name
    assert input_file.read_text() == output_file.read_text()

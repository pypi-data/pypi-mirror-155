from pathlib import Path
from typing import Callable, Tuple

import pytest
import typer

from cliconf import configure
from cliconf.main import CLIConf
from tests.dirutils import create_temp_path
from tests.fixtures.app_settings import (
    SETTINGS_ALL_OPTIONAL_JSON,
    SETTINGS_ONE_YAML,
    SETTINGS_TWO_PY,
)

single_command_yaml_cliconf = CLIConf(name="single_command_yaml")


@single_command_yaml_cliconf.command()
@configure(pyappconf_settings=SETTINGS_ONE_YAML)
def my_cli_func_one_yaml(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
):
    print(a, b, c)


@pytest.fixture
def single_command_yaml_cliconf_in_temp_dir() -> Tuple[CLIConf, Path]:
    with create_temp_path() as temp_path:
        settings = SETTINGS_ONE_YAML.copy(custom_config_folder=temp_path)
        temp_dir_cliconf = CLIConf(name="single_command_yaml_in_temp_dir")

        @temp_dir_cliconf.command()
        @configure(pyappconf_settings=settings)
        def my_cli_func_one_yaml(
            a: str,
            b: int = typer.Argument(..., help="b help"),
            c: float = typer.Option(3.2, help="c help"),
        ):
            print(a, b, c)

        yield temp_dir_cliconf, temp_path


single_command_py_cliconf = CLIConf(name="single_command_py")


def default_func_for_single_command_py(c: float) -> str:
    return f"default {c}"


@single_command_py_cliconf.command()
@configure(pyappconf_settings=SETTINGS_TWO_PY)
def my_cli_func_two_py(
    a: str,
    b: int = typer.Argument(..., help="b help"),
    c: float = typer.Option(3.2, help="c help"),
    d: Callable[[float], str] = default_func_for_single_command_py,
):
    print(a, b, c, d(c))


@pytest.fixture
def single_command_py_cliconf_in_temp_dir() -> Tuple[CLIConf, Path]:
    with create_temp_path() as temp_path:
        settings = SETTINGS_TWO_PY.copy(custom_config_folder=temp_path)
        temp_dir_cliconf = CLIConf(name="single_command_py_in_temp_dir")

        @temp_dir_cliconf.command()
        @configure(pyappconf_settings=settings)
        def my_cli_func_two_py(
            a: str,
            b: int = typer.Argument(..., help="b help"),
            c: float = typer.Option(3.2, help="c help"),
            d: Callable[[float], str] = default_func_for_single_command_py,
        ):
            print(a, b, c, d(c))

        yield temp_dir_cliconf, temp_path


single_command_all_optional_json_cliconf = CLIConf(
    name="single_command_all_optional_json"
)


@single_command_all_optional_json_cliconf.command()
@configure(pyappconf_settings=SETTINGS_ALL_OPTIONAL_JSON)
def my_cli_func_all_optional_json(
    a: str = typer.Option("abc", help="a help"),
    b: int = typer.Option(123, help="b help"),
):
    print(a, b)


if __name__ == "__main__":
    single_command_py_cliconf()

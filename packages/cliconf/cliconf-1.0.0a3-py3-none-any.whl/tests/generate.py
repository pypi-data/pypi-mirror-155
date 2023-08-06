from typing import Callable

from pyappconf import BaseConfig

from cliconf.ext_pyappconf import save_model
from tests.fixtures.app_settings import SETTINGS_ONE_YAML, SETTINGS_TWO_PY
from tests.fixtures.cliconfs import (
    default_func_for_single_command_py,
    my_cli_func_two_py,
)


class ConfigOne(BaseConfig):
    a: str
    b: int
    c: float = 45.6

    _settings = SETTINGS_ONE_YAML


def generate_config_one():
    ConfigOne(a="a from config", b=1000).save()


def custom_d_func(c: float) -> str:
    return f"custom {c}"


def generate_config_two_py():
    ConfigTwo = my_cli_func_two_py.model_cls
    current_folder = ConfigTwo._settings.custom_config_folder
    settings = ConfigTwo._settings.copy(custom_config_folder=current_folder / "plain")
    obj = ConfigTwo(settings=settings)
    save_model(obj, my_cli_func_two_py)


def generate_config_two_py_with_overrides():
    ConfigTwo = my_cli_func_two_py.model_cls
    current_folder = ConfigTwo._settings.custom_config_folder
    current_imports = ConfigTwo._settings.py_config_imports
    new_imports = [*current_imports, "from tests.generate import custom_d_func"]
    settings = ConfigTwo._settings.copy(
        py_config_imports=new_imports, custom_config_folder=current_folder / "overrides"
    )
    obj = ConfigTwo(c=123.4, d=custom_d_func, settings=settings)
    save_model(obj, my_cli_func_two_py)


if __name__ == "__main__":
    generate_config_one()
    generate_config_two_py()
    generate_config_two_py_with_overrides()

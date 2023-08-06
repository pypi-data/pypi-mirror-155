from pyappconf import ConfigFormats

from cliconf import CLIAppConfig
from tests.config import CONFIGS_DIR

SETTINGS_ONE_YAML = CLIAppConfig(
    app_name="MyApp",
    config_name="one",
    custom_config_folder=CONFIGS_DIR,
    default_format=ConfigFormats.YAML,
)


SETTINGS_TWO_PY = CLIAppConfig(
    app_name="MyApp",
    config_name="two",
    custom_config_folder=CONFIGS_DIR,
    default_format=ConfigFormats.PY,
    py_config_imports=[
        "from tests.fixtures.cliconfs import my_cli_func_two_py, default_func_for_single_command_py",
    ],
)

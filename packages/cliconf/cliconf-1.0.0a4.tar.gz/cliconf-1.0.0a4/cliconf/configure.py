import functools
import inspect
from types import FunctionType
from typing import Callable, List, Type

from pyappconf import AppConfig, BaseConfig

from cliconf.dynamic_config import (
    create_dynamic_config_class_from_function,
    filter_func_args_and_kwargs_to_get_user_passed_data,
)
from cliconf.ext_typer import get_arg_names_that_can_be_processed_by_typer
from cliconf.settings import DEFAULT_SETTINGS, CLIConfSettings


class _ModelContainer:
    def __init__(self):
        # Use a mutable container so that function can mutate
        self._models: List[Type[BaseConfig]] = []

    @property
    def model_cls(self) -> Type[BaseConfig]:
        return self._models[0]

    def set_model_cls(self, model_cls: Type[BaseConfig]):
        if len(self._models) > 0:
            self._models.pop()
        self._models.append(model_cls)

    model: Type[BaseConfig]


def configure(
    pyappconf_settings: AppConfig,
    cliconf_settings: CLIConfSettings = DEFAULT_SETTINGS,
) -> Callable:
    def actual_decorator(func: FunctionType):
        model_cls = create_dynamic_config_class_from_function(
            func,
            pyappconf_settings,
            cliconf_settings.base_cls,
            make_optional=cliconf_settings.make_fields_optional,
        )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Load the config, overriding with any user passed args
            user_passed_data = filter_func_args_and_kwargs_to_get_user_passed_data(
                func, args, kwargs
            )
            config = model_cls.load_or_create(model_kwargs=user_passed_data)
            return func(**config.dict(exclude={"settings"}))

        # Attach the generated config model class to the function, so it can be imported in
        # the py config format
        wrapper.model_cls = model_cls  # type: ignore

        # Also attach the settings to the function, so it can be used by the typer instance
        # to customize the options to add the --config-gen option
        wrapper.pyappconf_settings = pyappconf_settings  # type: ignore
        wrapper.cliconf_settings = cliconf_settings  # type: ignore

        # Override call signature to exclude any variables that cannot be processed by typer
        # Otherwise typer will fail while trying to create the click command.
        # These excluded values will come only from pyappconf and not from CLI.
        typer_args = get_arg_names_that_can_be_processed_by_typer(func)
        sig = inspect.signature(func)
        typer_sig = sig.replace(
            parameters=tuple(
                val for name, val in sig.parameters.items() if name in typer_args
            )
        )
        wrapper.__signature__ = typer_sig  # type: ignore

        return wrapper

    return actual_decorator

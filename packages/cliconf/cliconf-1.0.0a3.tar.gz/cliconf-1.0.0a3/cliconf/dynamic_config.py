import inspect
import typing
import warnings
from types import FunctionType
from typing import Any, Dict, Optional, Sequence, Type, no_type_check

from pyappconf import AppConfig, BaseConfig
from pydantic import create_model
from typing_extensions import TypeGuard

from cliconf.arg_store import ARGS_STORE
from cliconf.command_name import get_command_name
from cliconf.dynamic_config_name import dynamic_model_class_name
from cliconf.ext_pyappconf import create_cli_base_config_class
from cliconf.ext_typer import is_typer_parameter_info


@no_type_check
def create_dynamic_config_class_from_function(
    func: FunctionType,
    settings: AppConfig,
    base_cls: Optional[Type[BaseConfig]] = None,
    make_optional: bool = True,
) -> Type[BaseConfig]:
    """
    Create a BaseConfig class from a function.
    """
    base_cls = base_cls or create_cli_base_config_class(BaseConfig, settings)
    (
        args,
        _,
        varkw,
        defaults,
        kwonlyargs,
        kwonlydefaults,
        annotations,
    ) = inspect.getfullargspec(func)
    defaults = defaults or []
    args = args or []

    non_default_args = len(args) - len(defaults)
    defaults = (...,) * non_default_args + defaults

    keyword_only_params = {
        param: (
            _extract_type(annotations.get(param), make_optional),
            _extract_default(kwonlydefaults.get(param), make_optional),
        )
        for param in kwonlyargs
    }
    params = {
        param: (
            _extract_type(annotations.get(param), make_optional),
            _extract_default(default, make_optional),
        )
        for param, default in zip(args, defaults)
    }

    with warnings.catch_warnings():
        warnings.filterwarnings(
            action="ignore",
            category=RuntimeWarning,
            message='fields may not start with an underscore, ignoring "_settings"',
        )

        model_cls = create_model(
            dynamic_model_class_name(func),
            __base__=base_cls,
            **params,
            **keyword_only_params,
            settings=settings,
            _settings=settings,
        )
    return model_cls


def filter_func_args_and_kwargs_to_get_user_passed_data(
    func: FunctionType,
    func_args: Sequence[Any],
    func_kwargs: Dict[str, Any],
) -> Dict[str, Any]:
    args_kwargs = dict(zip(func.__code__.co_varnames[1:], func_args))
    args_kwargs.update(func_kwargs)
    # Get user passed args from command line via args store
    args_store = ARGS_STORE[get_command_name(func.__name__)]
    user_kwargs = args_store.params
    return user_kwargs


def _extract_default(value: Any, make_optional: bool) -> Any:
    underlying_value = _extract_from_typer_parameter_info_if_necessary(value)
    if not make_optional:
        return underlying_value
    return underlying_value if underlying_value is not ... else None


def _extract_from_typer_parameter_info_if_necessary(value: Any) -> Any:
    if is_typer_parameter_info(value):
        return value.default
    return value


@no_type_check
def _extract_type(typ: Optional[type], make_optional: bool) -> type:
    if typ is None:
        return Any

    if not make_optional:
        return typ

    if _is_optional(typ):
        return typ

    # Wrap type in Optional if it is not already
    return Optional[typ]


def _is_optional(typ: type) -> TypeGuard[Type[Optional[Any]]]:
    return typing.get_origin(typ) is typing.Union and type(None) in typing.get_args(typ)

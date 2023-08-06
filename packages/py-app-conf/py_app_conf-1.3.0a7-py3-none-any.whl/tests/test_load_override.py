import os
from pathlib import Path

import pytest

from pyappconf import ConfigFormats
from tests.config import (
    JSON_PATH,
    PY_CONFIG_PATH,
    PYPROJECT_TOML_MIXED_CONFIG_PATH,
    TOML_PATH,
    YAML_PATH,
)
from tests.fixtures.loader_func import LoaderFunc, loader_func
from tests.fixtures.model import get_model_classes, get_model_object


@pytest.mark.parametrize("config_format", list(ConfigFormats))
def test_load_with_kwarg_and_env_overrides(
    config_format: ConfigFormats, loader_func: LoaderFunc
):
    config_path = _get_config_path_for_format(config_format)
    config_name = _get_config_name_for_format(config_format, config_path)
    os.environ["MYAPP_STRING"] = "abc"
    os.environ["MYAPP_INT_TUPLE"] = "[4, 5, 6]"

    OrigConfig, _ = get_model_classes()
    settings = OrigConfig._settings_with_overrides(
        default_format=config_format,
        custom_config_folder=config_path.parent,
        config_name=config_name,
    )

    class MyConfig(OrigConfig):
        _settings = settings

    model_object = get_model_object(
        string="abc", int_tuple=(40, 50, 60), integer=10, settings=settings
    )

    loader = loader_func.get_loader(MyConfig)
    loaded_object = loader(
        config_path, model_kwargs=dict(int_tuple=(40, 50, 60), integer=10)
    )

    del os.environ["MYAPP_STRING"]
    del os.environ["MYAPP_INT_TUPLE"]
    assert model_object == loaded_object

    # User passed should override env or config file
    # env should override config file
    # config file should be used if not overrided
    assert loaded_object.string == "abc"  # loaded from env, overriding config
    assert loaded_object.int_tuple == (
        40,
        50,
        60,
    )  # loaded from user kwarg, overriding env and config
    assert loaded_object.integer == 10  # loaded from user kwarg, overriding config
    assert loaded_object.str_list == ["a", "b", "c"]  # loaded from config


def _get_config_path_for_format(config_format: ConfigFormats) -> Path:
    if config_format == ConfigFormats.JSON:
        return JSON_PATH
    elif config_format == ConfigFormats.YAML:
        return YAML_PATH
    elif config_format == ConfigFormats.TOML:
        return TOML_PATH
    elif config_format == ConfigFormats.PY:
        return PY_CONFIG_PATH
    elif config_format == ConfigFormats.PYPROJECT:
        return PYPROJECT_TOML_MIXED_CONFIG_PATH
    else:
        raise NotImplementedError(f"{config_format} has no corresponding path")


def _get_config_name_for_format(config_format: ConfigFormats, config_path: Path) -> str:
    if config_format == ConfigFormats.PYPROJECT:
        return "config"
    else:
        return config_path.with_suffix("").name

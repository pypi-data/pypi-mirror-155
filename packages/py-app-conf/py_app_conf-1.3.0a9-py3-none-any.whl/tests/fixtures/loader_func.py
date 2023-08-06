from enum import Enum
from pathlib import Path
from typing import Callable, Type

import pytest

from pyappconf import BaseConfig


class LoaderFunc(str, Enum):
    LOAD = "load"
    LOAD_OR_CREATE = "load_or_create"
    LOAD_RECURSIVE = "load_recursive"

    def get_loader(self, config_cls: Type[BaseConfig]) -> Callable:
        base_loader = getattr(config_cls, self.value)
        if self == LoaderFunc.LOAD_RECURSIVE:
            # Make recursive loader load the folder containing the config file
            def load_recursive_with_config_parent(path: Path, *args, **kwargs):
                return base_loader(path.parent, *args, **kwargs)

            return load_recursive_with_config_parent
        return base_loader


@pytest.fixture(params=list(LoaderFunc))
def loader_func(request) -> LoaderFunc:
    return request.param

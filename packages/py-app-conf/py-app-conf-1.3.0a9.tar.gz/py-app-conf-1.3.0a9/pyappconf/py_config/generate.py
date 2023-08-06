import datetime
import types
from enum import Enum
from pathlib import Path
from typing import Any, Final, Sequence, Set, Tuple
from uuid import UUID

import black
import isort
from pydantic import BaseModel
from pydantic.fields import ModelField


def pydantic_model_to_python_config_file(
    model: BaseModel,
    imports: Sequence[str],
    exclude_fields: Sequence[str] = tuple(),
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    unformatted = _pydantic_model_to_python_config_file(model, imports, exclude_fields)
    # Format the python config file with black.
    formatted = _format_python_config_file(unformatted)
    return formatted


def pydantic_model_to_python_config_stub_file(
    model: BaseModel,
    imports: Sequence[str],
    exclude_fields: Sequence[str] = tuple(),
    generate_model_class: bool = False,
) -> str:
    """
    Generate the stub file for the generated python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python stub file.
    """
    unformatted = _pydantic_model_to_python_config_stub_file(
        model, imports, generate_model_class, exclude_fields
    )
    # Format the python config file with black.
    formatted = _format_python_config_file(unformatted, is_stub=True)
    return formatted


def _format_python_config_file(unformatted: str, is_stub: bool = False) -> str:
    """
    Format a python config file.

    :param unformatted: The python config file.
    :return: The formatted python config file.
    """
    isort_formatted = isort.code(unformatted)
    # Format with black second, so it can reformat the imports
    black_formatted = black.format_str(isort_formatted, mode=_black_file_mode(is_stub))

    return black_formatted


def _black_file_mode(is_stub: bool) -> black.FileMode:
    """
    Get the black file mode.

    :param is_stub: Whether the file is a stub.
    :return: The black file mode.
    """
    if is_stub:
        return black.FileMode(line_length=80, is_pyi=True)
    return black.FileMode(line_length=80)


def _pydantic_model_to_python_config_file(
    model: BaseModel,
    imports: Sequence[str],
    exclude_fields: Sequence[str] = tuple(),
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    detected_stdlib_imports: Set[str] = set()
    # _build_attribute_value() will add imports to detected_stdlib_imports.
    attributes_str = _build_model_attributes(
        model, detected_stdlib_imports, exclude_fields
    )
    imports_str = "\n".join([*imports, *detected_stdlib_imports])
    name = model.__class__.__name__
    return f"""
{imports_str}

config = {name}({attributes_str})
""".strip()


def _pydantic_model_to_python_config_stub_file(
    model: BaseModel,
    imports: Sequence[str],
    generate_model_class: bool = False,
    exclude_fields: Sequence[str] = tuple(),
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    name = model.__class__.__name__
    if not generate_model_class:
        imports_str = "\n".join(imports)
        return f"""
{imports_str}

config: {name}
""".strip()

    detected_stdlib_imports: Set[str] = set()
    # _build_attribute_value() and _build_attribute_type() will add imports to detected_stdlib_imports.
    attributes_str = _build_model_class_attributes(
        model, detected_stdlib_imports, exclude_fields
    )
    detected_stdlib_imports.add("from pydantic import BaseModel")
    imports_str = "\n".join([*imports, *detected_stdlib_imports])

    return f"""
{imports_str}

class {name}(BaseModel):
{attributes_str}

config: {name}
""".strip()


def _build_model_attributes(
    model: BaseModel, stdlib_imports: Set[str], exclude_fields: Sequence[str] = tuple()
) -> str:
    """
    Build the attribute definition of a pydantic model.

    :param model: The pydantic model.
    :return: The attributes of the model.
    """
    attributes = ""
    field: ModelField
    for field_name, field in model.__fields__.items():
        if field_name in exclude_fields:
            continue
        value = getattr(model, field_name)
        attributes += (
            f"    {field_name} = {_build_attribute_value(value, stdlib_imports)},\n"
        )
    return attributes


def _build_model_class_attributes(
    model: BaseModel, stdlib_imports: Set[str], exclude_fields: Sequence[str] = tuple()
) -> str:
    """
    Build the attribute definition of a pydantic model class.

    :param model: The pydantic model.
    :return: The attributes of the model class.
    """
    attributes = ""
    field: ModelField
    for field_name, field in model.__fields__.items():
        if field_name in exclude_fields:
            continue
        value = getattr(model, field_name)
        attributes += f"    {field_name}: {_build_attribute_type(field, stdlib_imports)} = {_build_attribute_value(value, stdlib_imports)}\n"
    return attributes


CONTAINER_TYPES: Final[Tuple[str, ...]] = (
    "Mapping",
    "Dict",
    "List",
    "Set",
    "Tuple",
    "Generator",
    "Iterator",
    "AsyncGenerator",
    "AsyncIterator",
    "Optional",
    "Union",
    "Callable",
    "Sequence",
    "FrozenSet",
    "Iterable",
    "Deque",
    "DefaultDict",
    "Counter",
)

IMPORT_DATA_TYPES: Final[Tuple[str, ...]] = ("Any",)


def _build_attribute_type(field: ModelField, stdlib_imports: Set[str]) -> str:
    """
    Build the type of an attribute for a pydantic model class definition.

    :param value: A type class.
    :return: The code string representation of the type class.
    """
    # Use pydantic's type representation for __repr__ to convert to string
    # Not great to be using a private method, but there would be a lot of
    # logic to vendor.
    type_str = field._type_display()

    import_from_typing: Set[str] = set()
    for container_type in CONTAINER_TYPES:
        if container_type + "[" in type_str:
            import_from_typing.add(container_type)

    for data_type in IMPORT_DATA_TYPES:
        if data_type in type_str:
            import_from_typing.add(data_type)

    if import_from_typing:
        all_imports = ", ".join(import_from_typing)
        stdlib_imports.add(f"from typing import {all_imports}")
    return type_str


def _build_attribute_value(value: Any, stdlib_imports: Set[str]) -> str:
    """
    Build the attribute value of a pydantic model.

    :param value: The value of the attribute.
    :return: The value of the attribute.
    """
    if hasattr(value, "__pyconfig_repr__"):
        return value.__pyconfig_repr__()
    if isinstance(value, Enum):
        return f"{value.__class__.__name__}.{value.name}"
    elif isinstance(value, Path):
        stdlib_imports.add("from pathlib import Path")
        return f'Path("{value}")'
    elif isinstance(value, UUID):
        stdlib_imports.add("from uuid import UUID")
        return f'UUID("{value}")'
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, BaseModel):
        return repr(value)
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        stdlib_imports.add("import datetime")
        return repr(value)
    elif isinstance(value, types.FunctionType):
        return f"{value.__name__}"
    elif callable(value):
        raise ValueError(
            "Cannot convert generic callable to python config. Real functions defined with def are supported"
        )
    elif isinstance(value, list):
        return (
            f"[{', '.join(_build_attribute_value(v, stdlib_imports) for v in value)}]"
        )
    elif isinstance(value, tuple):
        return (
            f"({', '.join(_build_attribute_value(v, stdlib_imports) for v in value)})"
        )
    elif isinstance(value, dict):
        return f"{{{', '.join(f'{_build_attribute_value(k, stdlib_imports)}: {_build_attribute_value(v, stdlib_imports)}' for k, v in value.items())}}}"
    else:
        return str(value)

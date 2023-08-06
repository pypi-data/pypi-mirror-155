import datetime
import re
import types
from enum import Enum
from pathlib import Path
from typing import Any, Sequence, Set
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
        attributes += f"    {field_name}: {_build_attribute_type(field.type_, stdlib_imports)} = {_build_attribute_value(value, stdlib_imports)}\n"
    return attributes


TYPE_STR_RE = re.compile(r"<(class|enum) '([\w.]+)'>")


def _build_attribute_type(value: type, stdlib_imports: Set[str]) -> str:
    """
    Build the type of an attribute for a pydantic model class definition.

    :param value: A type class.
    :return: The code string representation of the type class.
    """
    str_value = str(value)
    # Parse the format <class 'str'> to str using a regular expression.
    match = TYPE_STR_RE.match(str_value)
    if match:
        fully_qualified_path = match.group(2)
        # fully_qualified_path could be just e.g. str or could be e.g. my.package.Something
        # We are assuming that the user is using a direct import for any custom types, so
        # extract only the name from the fully qualified path.
        import_name = fully_qualified_path.split(".")[-1]
        return import_name
    # May be in format typing.Callable[[], str]
    if "typing" in str_value:
        stdlib_imports.add("import typing")
        return str_value
    raise ValueError("Unsupported type class: " + str(value))


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

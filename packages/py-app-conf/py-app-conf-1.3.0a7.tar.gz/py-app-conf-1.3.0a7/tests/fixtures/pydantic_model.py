import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Tuple
from uuid import UUID

import pytest
from pydantic import BaseModel, Field

from tests.fixtures.data import get_default_data


class MyEnum(str, Enum):
    ONE = "one"
    TWO = "two"


class SubModel(BaseModel):
    a: str
    b: float


class MyModel(BaseModel):
    string: str
    integer: int
    custom: SubModel
    dictionary: Dict[str, SubModel]
    str_list: List[str]
    int_tuple: Tuple[int, ...]
    uuid: UUID
    date: datetime.date
    time: datetime.datetime

    default_string: str = "woo"
    default_custom: SubModel = SubModel(a="yeah", b=5.6)
    default_enum: MyEnum = MyEnum.ONE
    default_enum_list: List[MyEnum] = Field(
        default_factory=lambda: [MyEnum.ONE, MyEnum.TWO]
    )
    default_uuid_list: List[UUID] = Field(
        default_factory=lambda: [UUID("a" * 32), UUID("b" * 32)]
    )
    default_time_with_tz: datetime.datetime = datetime.datetime(
        2022, 1, 1, tzinfo=datetime.timezone.utc
    )
    default_time_list: List[datetime.datetime] = Field(
        default_factory=lambda: [
            datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.min),
            datetime.datetime(2022, 1, 2, tzinfo=datetime.timezone.max),
        ]
    )
    default_date_list: List[datetime.date] = Field(
        default_factory=lambda: [
            datetime.date(2022, 1, 1),
            datetime.date(2022, 1, 2),
        ]
    )
    file_path: Path = Path("/a/b.txt")


def default_func():
    return "default"


class RequiredCallableClass:
    def __call__(self):
        return "required"

    def __pyconfig_repr__(self):
        return "required_callable"


required_callable = RequiredCallableClass()


class PythonFormatSpecificModel(MyModel):
    func: Callable[[], str]
    optional_func: Callable[[], str] = default_func


def get_pydantic_model_object() -> MyModel:
    all_kwargs = get_default_data()
    return MyModel(**all_kwargs)


def get_python_format_specific_model_object() -> PythonFormatSpecificModel:
    all_kwargs = get_default_data()
    all_kwargs["func"] = required_callable
    return PythonFormatSpecificModel(**all_kwargs)


@pytest.fixture
def pydantic_model_object() -> MyModel:
    yield get_pydantic_model_object()


@pytest.fixture
def python_format_specific_model_object() -> PythonFormatSpecificModel:
    yield get_python_format_specific_model_object()


PYTHON_FORMAT_IMPORT = "from tests.fixtures.pydantic_model import PythonFormatSpecificModel, SubModel, MyEnum, default_func, required_callable"

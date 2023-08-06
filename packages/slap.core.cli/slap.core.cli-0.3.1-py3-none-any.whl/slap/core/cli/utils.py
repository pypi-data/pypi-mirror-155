import textwrap
from typing import Any, Iterable, Optional, Type, TypeVar

T = TypeVar("T")


def first_of_type(it: Iterable[Any], type_: Type[T]) -> Optional[T]:
    return next((item for item in it if isinstance(item, type_)), None)


def format_docstring(docstring: str) -> str:
    first_line, remainder = (docstring or "").partition("\n")[::2]
    return (first_line.strip() + "\n" + textwrap.dedent(remainder)).strip()


def get_first_line(text: str) -> str:
    lines = text.splitlines()
    return lines[0] if lines else ""


def not_none(value: Optional[T]) -> T:
    if value is None:
        raise RuntimeError("expected not None")
    return value

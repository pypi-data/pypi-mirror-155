"""
Provides a type-hint based API for defining :module:`argparse` based argument parsers.
"""

import argparse
import copy
import dataclasses
from typing import (
    Any,
    Callable,
    ClassVar,
    Collection,
    Dict,
    Generic,
    List,
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

import typeapi
from nr.util.terminal.colors import StyleManager

from .argparse import ArgumentParser, Formatter
from .utils import first_of_type, format_docstring, get_first_line, not_none

T = TypeVar("T")
T_TypedArgsBase = TypeVar("T_TypedArgsBase", bound="TypedArgsBase")

type_handlers: Dict[Type, Callable[[str], Any]] = {}


@dataclasses.dataclass
class Argument:
    """Metadata for a field annotation in a :class:`TypedArgsBase`."""

    metavar: Optional[str] = None
    nargs: Union[int, str, None] = None
    default: Optional[Any] = None
    type: Optional[Callable[[str], Any]] = None
    help: Optional[str] = None


@dataclasses.dataclass
class Option(Argument):
    """Metadata for a field annotation in a :class:`TypedArgsBase`."""

    long_name: Optional[str] = None
    short_name: Optional[str] = None
    action: Optional[str] = None
    version: Optional[str] = None
    required: Optional[bool] = None


class Ignore:
    """Use as an annotation to ignore a field."""


@dataclasses.dataclass
class Subcommand:
    name: str
    help: Optional[str] = None  #: Long help
    description: Optional[str] = None  #: Short description
    usage: Optional[str] = None
    epilog: Optional[str] = None


class TypedArgsBase:
    """Base class for classes that describe their options using annotations in type hints."""

    #: Set to metadata for the subcommand if this parser represents one.
    __subcommand_metadata__: ClassVar[Optional[Subcommand]] = None

    #: A mapping of all the registered subcommands.
    __subcommands__: ClassVar[Dict[str, Type["TypedArgsBase"]]]

    #: Style for formatting hints.
    __style__: ClassVar[StyleManager] = StyleManager()
    __style__.add_style("u", attrs=["underline"])
    __style__.add_style("b", attrs=["bold"])
    __style__.add_style("i", attrs=["italic"])
    __style__.add_style("0", "black")
    __style__.add_style("1", "red")
    __style__.add_style("2", "green")
    __style__.add_style("3", "yellow")
    __style__.add_style("4", "blue")
    __style__.add_style("5", "magenta")
    __style__.add_style("6", "cyan")
    __style__.add_style("7", "white")

    def __init_subclass__(cls) -> None:
        cls.__subcommands__ = {}
        doc = cls.__doc__
        dataclasses.dataclass(cls)
        cls.__doc__ = doc

    @classmethod
    def _new_parser(cls, prog: Optional[str] = None) -> argparse.ArgumentParser:
        subcommands = [
            Formatter.SubcommandDetails(k, not_none(v.__subcommand_metadata__).description)
            for k, v in cls.__subcommands__.items()
        ]
        return ArgumentParser(prog=prog, formatter_class=lambda prog: Formatter(prog, subcommands))

    @classmethod
    def _build_parser(cls, parser: argparse.ArgumentParser) -> None:
        for field in fields(cls).values():
            metadata = field.metadata
            args: List[Any] = []
            kwargs: Dict[str, Any] = {}
            if isinstance(metadata, Option):  # Do this check before Argument because of subclassing
                args = [f"--{metadata.long_name or field.name.replace('_', '-')}"]
                if metadata.short_name:
                    args.append(f"-{metadata.short_name}")
                if metadata.action:
                    kwargs["action"] = metadata.action
                if metadata.version:
                    kwargs["version"] = metadata.version
                    if not metadata.action:
                        kwargs["action"] = "version"
                elif metadata.required is not None:
                    kwargs["required"] = metadata.required
            elif isinstance(metadata, Argument):
                args = []
            else:
                raise RuntimeError(type(metadata))
            if metadata.metavar:
                kwargs["metavar"] = metadata.metavar
            if metadata.nargs:
                kwargs["nargs"] = metadata.nargs
            if metadata.default is not None:
                kwargs["default"] = metadata.default
            if metadata.type:
                kwargs["type"] = metadata.type
            if metadata.help:
                kwargs["help"] = metadata.help
            parser.add_argument(*args, dest=field.name, **kwargs)

        if cls.__subcommands__:
            subparsers = parser.add_subparsers(  # type: ignore[call-overload]
                parser_class=lambda cls, **kw: cls._new_parser(**kw)
            )
            for command, subcommand in cls.__subcommands__.items():
                subparser = subparsers.add_parser(command, cls=subcommand)
                subcommand._build_parser(subparser)

        if cls.__doc__:
            parser.description = format_docstring(cls.__doc__)
            parser.description = cls.__style__.format(parser.description)

        parser.set_defaults(__build__=cls._parser_default)

    @classmethod
    def _parser_default(cls: Type[T_TypedArgsBase], args: argparse.Namespace) -> T_TypedArgsBase:
        kwargs = {}
        for field in fields(cls, with_parent=True).values():
            if isinstance(field.metadata, Option) and field.metadata.version:
                value = None
            else:
                value = getattr(args, field.name)
            kwargs[field.name] = value
        return cls(**kwargs)

    @classmethod
    def parser(cls: Type[T_TypedArgsBase]) -> "_ParserWrapper[T_TypedArgsBase]":
        parser = cls._new_parser()
        cls._build_parser(parser)
        return _ParserWrapper(parser)


class _ParserWrapper(Generic[T_TypedArgsBase]):
    def __init__(self, parser: argparse.ArgumentParser) -> None:
        self._parser = parser

    def error(self, message: str) -> NoReturn:
        self._parser.error(message)

    def print_usage(self) -> None:
        self._parser.print_usage()

    def parse_args(self, argv: Optional[List[str]] = None) -> T_TypedArgsBase:
        args = self._parser.parse_args(argv)
        return args.__build__(args)


def subcommand(
    name: str,
    help: Optional[str] = None,
    description: Optional[str] = None,
    usage: Optional[str] = None,
    epilog: Optional[str] = None,
) -> Callable[[T], T]:
    """Decorator for subclasses of a :class:`TypedArgsBase` subclass to mark them as a subcommand
    instead of an extension of the parser."""

    def decorator(type_: T) -> T:
        nonlocal help, description
        assert isinstance(type_, type) and issubclass(type_, TypedArgsBase)
        bases = [base for base in type_.__bases__ if issubclass(base, TypedArgsBase)]
        if len(bases) != 1:
            raise RuntimeError(f"expected exactly one base for subcommand, got {len(bases)}")
        help = format_docstring(help or type_.__doc__ or "")
        help = type_.__style__.format(help)
        description = description or get_first_line(help)
        type_.__subcommand_metadata__ = Subcommand(name, help, description, usage, epilog)
        bases[0].__subcommands__[name] = type_
        return cast(T, type_)

    return decorator


@dataclasses.dataclass
class Field:
    name: str
    type: typeapi.Hint
    metadata: Union[Option, Argument]


def fields(type_: Type[TypedArgsBase], with_parent: bool = False) -> Dict[str, Field]:
    results = {}

    if not type_.__subcommand_metadata__ or with_parent:
        bases = [base for base in type_.__bases__ if issubclass(base, TypedArgsBase)]
        for base in bases:
            results.update(fields(base, with_parent))

    for key, value in type_.__annotations__.items():
        if key.startswith("__"):
            continue
        hint = typeapi.of(value)
        if isinstance(hint, typeapi.ClassVar):
            continue
        metadata: Union[Argument, Option, None] = None
        if isinstance(hint, typeapi.Annotated):
            if first_of_type(hint.metadata, Ignore):
                continue
            metadata = copy.copy(first_of_type(hint.metadata, Argument) or first_of_type(hint.metadata, Option))
            hint = hint.wrapped
        metadata = metadata or Option()

        # Infer defaults.

        is_flag = isinstance(metadata, Option) and isinstance(hint, typeapi.Type) and hint.type is bool

        required: Optional[bool] = None
        if isinstance(hint, typeapi.Union) and hint.has_none_type() and len(hint.types) == 2:  # Check for Optional.
            required = False
            hint = hint.without_none_type()
        elif isinstance(hint, typeapi.Type):
            required = metadata.default is None
        if isinstance(metadata, Option) and metadata.required is None and not is_flag:
            metadata.required = required

        if isinstance(metadata, Option) and not metadata.action and is_flag:
            metadata.action = "store_true"

        if not isinstance(hint, typeapi.Type) and not metadata.type:
            raise ValueError(f"cannot auto detect type converter for field {type_.__name__}.{key}: {hint}")
        if (
            metadata.type is None
            and isinstance(hint, typeapi.Type)
            and (
                type(metadata) is Argument
                or (
                    isinstance(metadata, Option)
                    and (not metadata.version and metadata.action not in ("count", "store_true", "store_false"))
                )
            )
        ):
            if issubclass(hint.type, Collection):
                item_type = hint.args[0].type if hint.args and isinstance(hint.args[0], typeapi.Type) else None
                if not item_type:
                    raise ValueError(
                        f"cannot auto detect type converter field for items of {type_.__name__}.{key}: {hint}"
                    )
                metadata.type = item_type
            else:
                metadata.type = hint.type

        results[key] = Field(key, hint, metadata)

    return results

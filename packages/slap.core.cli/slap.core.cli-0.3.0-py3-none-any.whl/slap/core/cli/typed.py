"""
Provides a type-hint based API for defining :module:`argparse` based argument parsers.
"""

import argparse
import dataclasses
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type, TypeVar, Union, cast

import typeapi

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
    required: bool = False


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
                if metadata.required:
                    kwargs["required"] = metadata.required
            elif isinstance(metadata, Argument):
                args = []
                if metadata.nargs:
                    kwargs["nargs"] = metadata.nargs
                if metadata.default:
                    kwargs["default"] = metadata.default
                if metadata.type:
                    kwargs["type"] = metadata.type
                if metadata.help:
                    kwargs["help"] = metadata.help
            else:
                raise RuntimeError(type(metadata))
            if (
                kwargs.get("type") is None
                and isinstance(field.type, typeapi.Type)
                and kwargs.get("action") not in ("version", "count")
            ):
                kwargs["type"] = field.type.type
            parser.add_argument(*args, dest=field.name, **kwargs)

        if cls.__subcommands__:
            subparsers = parser.add_subparsers(  # type: ignore[call-overload]
                parser_class=lambda cls, **kw: cls._new_parser(**kw)
            )
            for command, subcommand in cls.__subcommands__.items():
                subparser = subparsers.add_parser(command, cls=subcommand)
                subcommand._build_parser(subparser)
                subparser.set_defaults(__build=subcommand._parser_default)

        if cls.__doc__:
            parser.description = cls.__doc__

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
    def parse(cls: Type[T_TypedArgsBase]) -> T_TypedArgsBase:
        parser = cls._new_parser()
        cls._build_parser(parser)
        args = parser.parse_args()
        if hasattr(args, "__build"):
            return getattr(args, "__build")(args)
        return cls._parser_default(args)


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
        assert isinstance(type_, type)
        bases = [base for base in type_.__bases__ if issubclass(base, TypedArgsBase)]
        if len(bases) != 1:
            raise RuntimeError(f"expected exactly one base for subcommand, got {len(bases)}")
        help = format_docstring(help or type_.__doc__ or "")
        description = description or get_first_line(help)
        type_.__subcommand_metadata__ = Subcommand(name, help, description, usage, epilog)  # type: ignore
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
            metadata = first_of_type(hint.metadata, Argument) or first_of_type(hint.metadata, Option)
            hint = hint.wrapped
        if not isinstance(hint, typeapi.Type) and (not metadata or not metadata.type):
            raise ValueError(f"cannot auto detect type converter for field {type_.__name__}.{key}: {hint}")
        if not metadata:
            metadata = Option()
        results[key] = Field(key, hint, metadata)

    return results

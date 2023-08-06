import abc
import argparse
from typing import TYPE_CHECKING, Any, Dict, Optional

from slap.core.cli.utils import format_docstring, get_first_line

if TYPE_CHECKING:
    from .app import CliApp
    from .features import FeatureHub


class BaseCommand(abc.ABC):
    """Pure interface for CLI commands."""

    _app: Optional["CliApp"] = None
    _name: Optional[str] = None
    _parent: Optional["BaseCommand"] = None
    _parser: Optional[argparse.ArgumentParser] = None

    def __repr__(self) -> str:
        if self._name is not None:
            full_name = self.get_full_name()
        else:
            full_name = "<unnamed>"
        return f"{type(self).__name__}({full_name!r})"

    def get_app(self) -> "CliApp":
        if self._app:
            return self._app
        if self._parent:
            return self._parent.get_app()
        raise RuntimeError("BaseCommand._app is not set (did you add the command to an app?)")

    def get_parser(self, features: Optional["FeatureHub"] = None) -> argparse.ArgumentParser:
        if self._parser is None:
            self._parser = self.get_app().new_argument_parser(self, features)
        return self._parser

    def get_name(self) -> str:
        assert self._name is not None, "BaseCommand._name is not set (did you add the command to a group?)"
        return self._name

    def get_full_name(self) -> str:
        if self._parent:
            return f"{self._parent.get_full_name()} {self._name}"
        return self.get_name()

    @abc.abstractmethod
    def get_description(self) -> str:
        ...

    @abc.abstractmethod
    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        ...

    @abc.abstractmethod
    def execute(self, args: Any) -> Optional[int]:
        ...


class Group(BaseCommand):
    def __init__(self, description: Optional[str] = None, help: Optional[str] = None) -> None:
        self._description = description
        self._help = help
        self._subcommands: Dict[str, BaseCommand] = {}

    def add_command(self, name: str, command: BaseCommand) -> None:
        command._name = name
        command._parent = self
        self._subcommands[name] = command

    def get_description(self) -> str:
        return self._description or get_first_line(self._help or "")

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.description = self._help
        if self._subcommands:
            parser.add_argument("cmd", nargs="?", choices=self._subcommands.keys(), help="the subcommand to execute")
            parser.add_argument("argv", metavar="...", nargs=argparse.REMAINDER, help="arguments for the subcommand")

    def execute(self, args: Any) -> int:
        if self._subcommands and args.cmd:
            command = self._subcommands[args.cmd]
            return self.get_app().dispatch(command, args.argv, None)
        else:
            self.get_parser().print_help()
            return 0


class Command(BaseCommand):
    def get_description(self) -> str:
        return get_first_line(format_docstring(self.__doc__ or ""))

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.description = format_docstring(self.__doc__ or "")

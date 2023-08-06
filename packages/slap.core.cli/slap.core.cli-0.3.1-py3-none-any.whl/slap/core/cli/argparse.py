import argparse
import dataclasses
import os
import re
import sys
from typing import Collection, Iterable, NoReturn, Optional, TypeVar

from termcolor import colored

T = TypeVar("T")


def get_terminal_width(fallback: int = 100) -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        try:
            return int(os.getenv("COLUMNS", ""))
        except ValueError:
            return fallback


class Formatter(argparse.RawTextHelpFormatter):
    """Formatter class that injects subcommand details into the formatting output."""

    @dataclasses.dataclass
    class SubcommandDetails:
        name: str
        description: Optional[str] = None

    def __init__(self, prog: str, subcommands: Optional[Collection[SubcommandDetails]] = None) -> None:
        width = get_terminal_width()
        max_help_position = max(30, width // 2)
        super().__init__(prog, width=width, max_help_position=max_help_position)
        self.__subcommands = subcommands
        self.__add_text_count = 0

    def __update_action_max_length(self, length: int) -> None:
        self._action_max_length = max(self._action_max_length, self._current_indent + length)

    def __get_help_position(self) -> int:
        return min(self._action_max_length + 2, self._max_help_position)

    def _format_subcommand(self, command: SubcommandDetails) -> str:
        action_width = self.__get_help_position() - 2 - self._current_indent
        # TODO (@niklas.rosenstein): Move command description to next line if command name is too long.
        return (
            f"{' ' * self._current_indent}{colored(command.name.ljust(action_width), 'cyan')}  "
            f"{command.description or ''}\n"
        )

    def add_subcommand(self, command: SubcommandDetails) -> None:
        assert command is not None
        self.__update_action_max_length(len(command.name))
        self._add_item(self._format_subcommand, (command,))

    # argparse.HelpFormatter

    def add_text(self, text: Optional[str]) -> None:
        # NOTE (@niklas.rosenstein): We use this to identify if we're formatting usage vs. help.
        self.__add_text_count += 1
        return super().add_text(text)

    def start_section(self, heading: Optional[str]) -> None:
        return super().start_section(colored(heading, attrs=["bold"]) if heading is not None else None)

    def format_help(self) -> str:
        if self.__subcommands and self.__add_text_count >= 2:
            self.start_section("subcommands")
            for command in self.__subcommands:
                self.add_subcommand(command)
            self.end_section()
        result = super().format_help()
        if self.__add_text_count >= 2:
            result += "\n"
        return result

    def _format_usage(
        self,
        usage: str,
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: Optional[str],
    ) -> str:
        usage = super()._format_usage(usage, actions, groups, prefix)
        usage = re.sub(r"^usage:", colored("usage:", "blue", attrs=["bold"]), usage)
        return usage


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_usage(sys.stderr)
        print(colored("error:", "red", attrs=["bold"]), message, file=sys.stderr)
        sys.exit(2)

import argparse
import dataclasses
import shlex
import sys
from typing import Any, Collection, List, Optional, Tuple

from .command import BaseCommand, Command, Group


def find_command(argv: List[str], command: BaseCommand) -> Tuple[List[str], BaseCommand]:
    """Find the command that is addressed with *argv*.

    Args:
        argv: The argument sequence to evaluate.
        command: The command to start evaluating the arguments from.
    Raises:
        ValueError: If the argument sequence cannot be resolved to a command.
    """

    if argv and isinstance(command, Group):
        subcommand = command._subcommands.get(argv[0])
        if not subcommand:
            return argv, command
        return find_command(argv[1:], subcommand)

    return argv, command


class CompletionCommand(Command):
    """completion backend for bash"""

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("comp_line", help="the $COMP_LINE value", nargs="?")
        parser.add_argument("--bash", action="store_true", help="print the code to enable completion for bash")
        parser.add_argument(
            "--prog", help="program prefix for completion [default: %(default)s]", default=self.get_app().name
        )

    def execute(self, args: Any) -> int:
        if args.bash and args.comp_line:
            self.get_parser().error("--bash option cannot be combined with comp_line argument")

        if args.bash:
            self.get_app().root._name = args.prog
            print(f'_{args.prog}() {{ COMPREPLY=($({self.get_full_name()} "$COMP_LINE")); }};')
            print(f"complete -F _{args.prog} {args.prog};")
            return 0

        if args.comp_line is None:
            self.get_parser().print_usage()
            return 0
        if not args.comp_line:
            return 0

        # NOTE (@NiklasRosenstein): Will fall back to sys.stdin if None is passed.
        argv = shlex.split(args.comp_line or "")
        if args.comp_line.endswith(" "):
            argv.append("")

        # Find the command for which the completion needs to be identified.
        last_arg = argv.pop()
        argv, target = find_command(argv[1:], self.get_app().root)
        argv.append(last_arg)

        parser = target.get_parser()

        if argv:
            consumer = ArgConsumer(parser._actions, argv)
            info = consumer.get_completion_info()
            if info:
                print("\n".join(info.values))

        return 0


@dataclasses.dataclass
class CompletionInfo:
    values: Collection[str]


class ArgConsumer:
    """Consumes an argument list per a list of :class:`argparse.Action`s. Note that the argument
    list that is being processed should contain an empty string as the last item to indicate that
    the cursor for completion is not located at the last argument."""

    def __init__(self, actions: List[argparse.Action], argv: List[str]) -> None:
        self.posititional_actions = [
            action for action in actions if not any(opt.startswith("-") for opt in action.option_strings)
        ]
        self.option_actions = [action for action in actions if action not in self.posititional_actions]
        assert len(argv) >= 1, argv
        self.argv = argv

    def _consume_args(self, action: argparse.Action) -> Optional[CompletionInfo]:
        """Consumes the arguments as per the given action's settings. If the action is determined
        to be consumed insufficiently, a :class:`CompletionInfo` will be returned."""

        assert self.argv

        # A remainder can take any number of arguments, independent of whether those arguments
        # look like options or note.
        if action.nargs in ("...", argparse.REMAINDER):
            self.argv, argv = [], self.argv
            return self._get_values(action, argv[-1])

        # Consume arguments until an option string is encountered.
        if action.nargs in ("+", "*", "?") or isinstance(action.nargs, int) or action.nargs is None:
            last_arg: Optional[str] = None
            num_args = 0
            max_args = (
                1
                if action.nargs is None
                else action.nargs
                if isinstance(action.nargs, int)
                else 1
                if action.nargs == "?"
                else None
            )
            while self.argv:
                if self.argv[0].startswith("-") or (max_args is not None and num_args >= max_args):
                    return None
                last_arg = self.argv.pop(0)
                num_args += 1
            assert last_arg is not None, action
            return self._get_values(action, last_arg)

        raise RuntimeError(f"Unexpected action.nargs: {action.nargs!r}")

    def _get_values(self, action: argparse.Action, prefix: str) -> CompletionInfo:
        values = []
        if action.choices:
            values = [value for value in action.choices if value.startswith(prefix)]
        return CompletionInfo(values)

    def _get_option(self, opt: str) -> Optional[argparse.Action]:
        # TODO (@NiklasRosenstein): Support --opt=value format (which is a single argument).
        for action in self.option_actions:
            if opt in action.option_strings:
                return action
        return None

    def get_completion_info(self) -> Optional[CompletionInfo]:
        action: Optional[argparse.Action]

        # If the last argument looks like an option, we provide help for available options.
        prefix = self.argv[-1]
        if prefix.startswith("-"):
            choices = []
            for action in self.option_actions:
                matches = [opt for opt in action.option_strings if opt.startswith(prefix)]
                long_matches = [opt for opt in matches if opt.startswith("--")]
                choices += long_matches or matches
            return CompletionInfo(choices)

        completion_info: Optional[CompletionInfo] = None
        while self.argv:
            if self.argv[0].startswith("-"):
                action = self._get_option(self.argv[0])
                if not action:
                    # We encountered an unknown option
                    print(f"note: unknown option: {self.argv[0]}", file=sys.stderr)
                    return None
                self.argv.pop(0)
            elif self.posititional_actions:
                completion_info = self._consume_args(self.posititional_actions.pop(0))
            else:
                # No positional arguments left to parse, so we don't know what to do with this.
                completion_info = None
                break

        # If a new positional action follows, we take it's completion info.
        if self.argv and self.posititional_actions:
            completion_info = self._consume_args(self.posititional_actions.pop(0))

        return completion_info

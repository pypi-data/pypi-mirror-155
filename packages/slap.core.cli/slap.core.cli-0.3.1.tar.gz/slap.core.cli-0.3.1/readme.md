# slap.core.cli

Extension of [`argparse`][0] to provide fast and customizable argument parsing.

  [0]: https://docs.python.org/3/library/argparse.html

## Features

* Minimal API; interact mostly with `argparse` or type hints
* Fast; because `argparse` is fast
* Completion; built-in support

## Usage (Command API)

```py
import argparse
from typing import Any, Optional

from slap.core.cli import CliApp, Command
from slap.core.cli.completion import CompletionCommand

class HelloCommand(Command):
    """ say hello to someone """

    def init_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("name")

    def execute(self, args: Any) -> Optional[int]:
        print(f"Hello, {args.name}!")

app = CliApp("minimal", "0.1.0")
app.add_command("hello", HelloCommand())
app.add_command("completion", CompletionCommand())
app.run()
```

Gives you the following CLI:

```
$ python examples/minimal.py
usage: minimal [-h] [-v] [--version] [{hello,completion}] ...

positional arguments:
  {hello,completion}  the subcommand to execute
  ...                 arguments for the subcommand

options:
  -h, --help          show this help message and exit
  -v, --verbose       increase the verbosity level
  --version           show program's version number and exit

subcommands:
  hello               say hello to someone
  completion          completion backend for bash
```

> __On Completion__
>
>
> You can run `python examples/minimal.py completion --bash` to get the code that should be run in your
> shell to enable completion features. However, you will need to make command available as a first-order
> command in your shell for completion to work (e.g. `minimal` instead of `python examples/minimal.py`).

## Usage (Typed API)

```py
from slap.core.cli.typed import Argument, Option, TypedArgsBase, subcommand
from typing import Annotated

class SayHelloArgs(TypedArgsBase):
    name: Annotated[str, Argument()]
    greeting: str
    version: Annotated[None, Option(version="1.0.0", short_name="V")]

args = SayHelloArgs.parse()
print(args)
```

Gives you the following CLI:

```
usage: test.py [-h] [--greeting GREETING] [--version] name

positional arguments:
  name

options:
  -h, --help           show this help message and exit
  --greeting GREETING
  --version, -V        show program's version number and exit
```

And running it gives:

```
$ python test.py John --greeting Hello
SayHelloArgs(name='John', greeting='Hello', version=None)
```

> Note: Completion is currently not supported for the typed API.

## Compatibility

Requires Python 3.7 or higher.

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cli']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0', 'typeapi>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'slap.core.cli',
    'version': '0.3.0',
    'description': 'Extension of `argparse` to provide fast and customizable argument parsing.',
    'long_description': '# slap.core.cli\n\nExtension of [`argparse`][0] to provide fast and customizable argument parsing.\n\n  [0]: https://docs.python.org/3/library/argparse.html\n\n## Features\n\n* Minimal API; interact mostly with `argparse` or type hints\n* Fast; because `argparse` is fast\n* Completion; built-in support\n\n## Usage (Command API)\n\n```py\nimport argparse\nfrom typing import Any, Optional\n\nfrom slap.core.cli import CliApp, Command\nfrom slap.core.cli.completion import CompletionCommand\n\nclass HelloCommand(Command):\n    """ say hello to someone """\n\n    def init_parser(self, parser: argparse.ArgumentParser) -> None:\n        parser.add_argument("name")\n\n    def execute(self, args: Any) -> Optional[int]:\n        print(f"Hello, {args.name}!")\n\napp = CliApp("minimal", "0.1.0")\napp.add_command("hello", HelloCommand())\napp.add_command("completion", CompletionCommand())\napp.run()\n```\n\nGives you the following CLI:\n\n```\n$ python examples/minimal.py\nusage: minimal [-h] [-v] [--version] [{hello,completion}] ...\n\npositional arguments:\n  {hello,completion}  the subcommand to execute\n  ...                 arguments for the subcommand\n\noptions:\n  -h, --help          show this help message and exit\n  -v, --verbose       increase the verbosity level\n  --version           show program\'s version number and exit\n\nsubcommands:\n  hello               say hello to someone\n  completion          completion backend for bash\n```\n\n> __On Completion__\n>\n>\n> You can run `python examples/minimal.py completion --bash` to get the code that should be run in your\n> shell to enable completion features. However, you will need to make command available as a first-order\n> command in your shell for completion to work (e.g. `minimal` instead of `python examples/minimal.py`).\n\n## Usage (Typed API)\n\n```py\nfrom slap.core.cli.typed import Argument, Option, TypedArgsBase, subcommand\nfrom typing import Annotated\n\nclass SayHelloArgs(TypedArgsBase):\n    name: Annotated[str, Argument()]\n    greeting: str\n    version: Annotated[None, Option(version="1.0.0", short_name="V")]\n\nargs = SayHelloArgs.parse()\nprint(args)\n```\n\nGives you the following CLI:\n\n```\nusage: test.py [-h] [--greeting GREETING] [--version] name\n\npositional arguments:\n  name\n\noptions:\n  -h, --help           show this help message and exit\n  --greeting GREETING\n  --version, -V        show program\'s version number and exit\n```\n\nAnd running it gives:\n\n```\n$ python test.py John --greeting Hello\nSayHelloArgs(name=\'John\', greeting=\'Hello\', version=None)\n```\n\n> Note: Completion is currently not supported for the typed API.\n\n## Compatibility\n\nRequires Python 3.7 or higher.\n',
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

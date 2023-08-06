import argparse
import json
import os
import textwrap
from argparse import Action, ArgumentError, RawTextHelpFormatter
from functools import lru_cache
from typing import Callable, Dict, Iterable, List, NamedTuple, Optional, Union
from wukong.utils.model_loading import import_string
from wukong.utils.helpers import partition


def lazy_load_command(import_path: str) -> Callable:
    """Create a lazy loader for command"""
    _, _, name = import_path.rpartition('.')

    def command(*args, **kwargs):
        func = import_string(import_path)
        return func(*args, **kwargs)

    command.__name__ = name

    return command


class DefaultHelpParser(argparse.ArgumentParser):
    """CustomParser to display help message"""

    def _check_value(self, action, value):
        """Override _check_value and check conditionally added command"""
        super()._check_value(action, value)

    def error(self, message):
        """Override error and use print_instead of print_usage"""
        self.print_help()
        self.exit(2, f'\n{self.prog} command error: {message}, see help above.\n')


_UNSET = object()


class Arg:
    """Class to keep information about command line argument"""

    def __init__(
            self,
            flags=_UNSET,
            help=_UNSET,
            action=_UNSET,
            default=_UNSET,
            nargs=_UNSET,
            type=_UNSET,
            choices=_UNSET,
            required=_UNSET,
            metavar=_UNSET,
            dest=_UNSET,
        ):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is _UNSET:
                continue
            if k in ("self", "flags"):
                continue

            self.kwargs[k] = v

    def add_to_parser(self, parser: argparse.ArgumentParser):
        """Add this argument to an ArgumentParser"""
        parser.add_argument(*self.flags, **self.kwargs)


class ActionCommand(NamedTuple):
    """Single CLI command"""

    name: str
    help: str
    func: Callable
    args: Iterable[Arg]
    description: Optional[str] = None
    epilog: Optional[str] = None


class GroupCommand(NamedTuple):
    """ClI command with subcommands"""

    name: str
    help: str
    subcommands: Iterable
    description: Optional[str] = None
    epilog: Optional[str] = None


CLICommand = Union[ActionCommand, GroupCommand]

ARG_YUQUE_API_TOKEN = Arg(
    ('-t', '--token',),
    help=(
        "Your yuque api key, this parameter must be provided if you never configure $wukong_HOME/wukong.cfg."
        "We recommend your to configure api key in $wukong_HOME/wukong.cfg."
    ),
    type=str,
)

ARG_YUQUE_API_UID = Arg(
    ('--uid',),
    help=(
        "Your yuque api key, this parameter must be provided if you never configure $wukong_HOME/wukong.cfg."
        "We recommend your to configure api key in $wukong_HOME/wukong.cfg."
    ),
    type=str,
)

ARG_YUQUE_SELF_USER = Arg(
    ('-u', '--user'),
    help=(
        "Username of your yuque account, and this must be a phone number. "
        "We recommend your to configure api key in $wukong_HOME/wukong.cfg."
    ),
    type=str,
)

ARG_YUQUE_SELF_PASSWORD = Arg(
    ('-p', '--password'),
    help=(
        "Password of your yuque account. "
        "We recommend your to configure api key in $wukong_HOME/wukong.cfg."
    ),
    type=str,
)

ARG_YUQUE_THUMBSUP_USER = Arg(
    ('-lu', '--like-user',),
    help=(
        "Username of other yuque account to thumbs up your docs, and this must be a phone number. "
        "We recommend your to configure api key in $wukong_HOME/wukong.cfg."
    ),
    type=str,
)

ARG_YUQUE_THUMBSUP_PASSWORD = Arg(
    ('-lp', '--like-password',),
    help=(
        "Password of other yuque account to thumbs up your docs. "
        "We recommend your to configure api key in yuque.cfg."
    ),
    type=str,
)

ARG_YUQUE_SEARCH_NUM = Arg(
    ('-n', '--num'),
    help=(
        "Limit num of docs for thumbs up YuQue account, "
        "or limit num of search users."
        "We recommend your to configure api key in yuque.cfg."
    ),
    type=int,
    default=1000
)

ARG_YUQUE_LIKE_NUM = Arg(
    ('-n', '--num'),
    help=(
        "Limit num of docs for thumbs up YuQue account, "
        "or limit num of search users."
        "We recommend your to configure api key in yuque.cfg."
    ),
    type=int,
    default=100
)

ARG_YUQUE_FOLLOW_COMMENT_NUM = Arg(
    ('-n', '--num'),
    help=(
        "Limit num of docs for thumbs up YuQue account, "
        "or limit num of search users."
        "We recommend your to configure api key in yuque.cfg."
    ),
    type=int,
    default=50
)

ARG_YUQUE_NOTE_NUM = Arg(
    ('-n', '--num'),
    help=(
        "Limit num of docs for thumbs up YuQue account, "
        "or limit num of search users."
        "We recommend your to configure api key in yuque.cfg."
    ),
    type=int,
    default=33
)


YUQUE_COMMANDS = (
    ActionCommand(
        name='init',
        help='Initialize a project for YuQue',
        description='Initialize a project named YuQueAssistant.',
        func=lazy_load_command('wukong.cli.commands.yuque.init'),
        args=(),
    ),
    ActionCommand(
        name='like',
        help='Thumbs up your docs by other YuQue accounts',
        description=(
            'Every other account can only thumbs up 100 docs every day, '
            'and each thumbs up for a document can obtain 7 rice. '
            'You can obtain max 2000 rice(about 285 docs) every week, '
            'so thumbs up 95 docs may be best for each account!'),
        func=lazy_load_command('wukong.cli.commands.yuque.like'),
        args=(ARG_YUQUE_API_TOKEN,
              ARG_YUQUE_API_UID,
              ARG_YUQUE_THUMBSUP_USER,
              ARG_YUQUE_THUMBSUP_PASSWORD,
              ARG_YUQUE_LIKE_NUM),
        ),
    ActionCommand(
        name='follow',
        help='Follow Other YuQue users',
        description=(
            'Follow each other account can obtain 2 rice, '
            'and max 100 rice every week in this behaviour, '
            'so you can follow 50 YuQue users every week.'),
        func=lazy_load_command('wukong.cli.commands.yuque.follow'),
        args=(ARG_YUQUE_SELF_USER, ARG_YUQUE_SELF_PASSWORD, ARG_YUQUE_FOLLOW_COMMENT_NUM),
    ),

    ActionCommand(
        name='unfollow',
        help='Unfollow YuQue users that you have followed',
        func=lazy_load_command('wukong.cli.commands.yuque.unfollow'),
        args=(ARG_YUQUE_SELF_USER, ARG_YUQUE_SELF_PASSWORD),
    ),
    ActionCommand(
        name='comment',
        help='Review other docs through your own YuQue account',
        description=(
            'Comment a document can obtain 2 rice each time, '
            'and review the same document repeatedly will not obtain rice again. '
            'so you can review 50 documents every week.'),
        func=lazy_load_command('wukong.cli.commands.yuque.comment'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_SELF_USER, ARG_YUQUE_SELF_PASSWORD, ARG_YUQUE_FOLLOW_COMMENT_NUM),
    ),
    ActionCommand(
        name='note',
        help='Take a note in YuQue Web Workbench',
        description=(
            'A note can obtain 2 rice each time, '
            'and max 100 rice for a week, '
            'so you can take max 50 notes every week.'),
        func=lazy_load_command('wukong.cli.commands.yuque.note'),
        args=(ARG_YUQUE_SELF_USER, ARG_YUQUE_SELF_PASSWORD, ARG_YUQUE_NOTE_NUM),
    ),
    ActionCommand(
        name='search-users',
        help='Search YuQue users',
        func=lazy_load_command('wukong.cli.commands.yuque.search_users'),
        args=(ARG_YUQUE_SELF_USER, ARG_YUQUE_SELF_PASSWORD, ARG_YUQUE_SEARCH_NUM),
    ),
    ActionCommand(
        name='search-docs',
        help='Search documents of YuQue users',
        func=lazy_load_command('wukong.cli.commands.yuque.search_docs'),
        args=(ARG_YUQUE_API_TOKEN, ARG_YUQUE_SEARCH_NUM),
    ),
)

wukong_commands: List[CLICommand] = [
    GroupCommand(
        name='yuque',
        help='Collect Rice Reward',
        subcommands=YUQUE_COMMANDS,
        ),
    ]

yuque_cli_commands: List[CLICommand] = [
    GroupCommand(
        name='yuque',
        help='Collect Rice Reward',
        subcommands=YUQUE_COMMANDS,
    ),
]

YUQUE_CLI_DICT: Dict[str, CLICommand] = {sp.name: sp for sp in yuque_cli_commands}

ALL_COMMANDS_DICT: Dict[str, CLICommand] = {sp.name: sp for sp in wukong_commands}


class wukongHelpFormatter(argparse.HelpFormatter):
    """
    Custom help formatter to display help message.
    It displays simple commands and groups of commands in separate sections.
    """

    def _format_action(self, action: Action):
        if isinstance(action, argparse._SubParsersAction):

            parts = []
            action_header = self._format_action_invocation(action)
            action_header = '%*s%s\n' % (self._current_indent, '', action_header)
            parts.append(action_header)

            self._indent()
            subactions = action._get_subactions()
            action_subcommands, group_subcommands = partition(
                lambda d: isinstance(ALL_COMMANDS_DICT[d.dest], GroupCommand), subactions
            )
            parts.append("\n")
            parts.append('%*s%s:\n' % (self._current_indent, '', "Groups"))
            self._indent()

            for subaction in group_subcommands:
                parts.append(self._format_action(subaction))

            self._dedent()
            parts.append("\n")
            parts.append('%*s%s:\n' % (self._current_indent, '', "Commands"))
            self._indent()

            for subaction in action_subcommands:
                parts.append(self._format_action(subaction))

            self._dedent()
            self._dedent()

            # return a single string
            return self._join_parts(parts)

        return super()._format_action(action)


@lru_cache(maxsize=None)
def get_parser(yuque_parser: bool = False) -> argparse.ArgumentParser:
    """Creates and returns command line argument parser"""
    parser = DefaultHelpParser(prog="wukong", formatter_class=wukongHelpFormatter)
    subparsers = parser.add_subparsers(dest='subcommand', metavar="GROUP_OR_COMMAND")
    subparsers.required = True

    command_dict = YUQUE_CLI_DICT if yuque_parser else ALL_COMMANDS_DICT
    subparser_list = command_dict.keys()
    sub_name: str

    for sub_name in sorted(subparser_list):
        sub: CLICommand = command_dict[sub_name]
        _add_command(subparsers, sub)

    return parser


def _sort_args(args: Iterable[Arg]) -> Iterable[Arg]:
    """Sort subcommand optional args, keep positional args"""

    def get_long_option(arg: Arg):
        """Get long option from Arg.flags"""
        return arg.flags[0] if len(arg.flags) == 1 else arg.flags[1]

    positional, optional = partition(lambda x: x.flags[0].startswith("-"), args)
    yield from positional
    yield from sorted(optional, key=lambda x: get_long_option(x).lower())


def _add_command(subparsers: argparse._SubParsersAction, sub: CLICommand) -> None:
    sub_proc = subparsers.add_parser(
        sub.name,
        help=sub.help,
        description=sub.description or sub.help,
        epilog=sub.epilog
    )
    sub_proc.formatter_class = RawTextHelpFormatter

    if isinstance(sub, GroupCommand):
        _add_group_command(sub, sub_proc)
    elif isinstance(sub, ActionCommand):
        _add_action_command(sub, sub_proc)
    else:
        raise Exception("Invalid command definition.")


def _add_action_command(sub: ActionCommand, sub_proc: argparse.ArgumentParser) -> None:
    for arg in _sort_args(sub.args):
        arg.add_to_parser(sub_proc)

    sub_proc.set_defaults(func=sub.func)


def _add_group_command(sub: GroupCommand, sub_proc: argparse.ArgumentParser) -> None:
    subcommands = sub.subcommands
    sub_subparsers = sub_proc.add_subparsers(dest="subcommand", metavar="COMMAND")
    sub_subparsers.required = True

    for command in sorted(subcommands, key=lambda x: x.name):
        _add_command(sub_subparsers, command)

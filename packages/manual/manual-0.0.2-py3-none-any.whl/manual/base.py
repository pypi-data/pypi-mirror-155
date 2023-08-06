"""
Base objects
"""

from string import Formatter
import os
from itertools import chain

from i2 import Sig

from manual.util import field_names_of_format_string, execute_command


def mk_command_runner(commands_template, name=None, *, step_by_step=False):
    """Make a python function from a sequence of templated system commands.

    :param commands_template: Multi-line string of commands or list of commands
    :param name: The name we want the output function to be called
    :param step_by_step: Set to True if we want the commands to be run one by one

    >>> mytest = mk_command_runner([
    ...     'export {env_var}="{value}"',
    ...     'echo {env_var}',
    ...     'unset {env_var}',
    ... ])
    >>> from inspect import signature
    >>> str(signature(mytest))
    '(env_var, value, *, _dry_run=False)'
    >>> mytest('__SOME_ENV_VAR_FOR_TESTING__', 'test 123')
    <BLANKLINE>
    (1/3)$ export __SOME_ENV_VAR_FOR_TESTING__="test 123"
    <BLANKLINE>
    (2/3)$ echo __SOME_ENV_VAR_FOR_TESTING__
    __SOME_ENV_VAR_FOR_TESTING__
    <BLANKLINE>
    <BLANKLINE>
    (3/3)$ unset __SOME_ENV_VAR_FOR_TESTING__
    """
    if isinstance(commands_template, list):
        commands_template = '\n'.join(commands_template)
    commands_template = commands_template.strip()
    sig = Sig(field_names_of_format_string(commands_template)) + '_dry_run'
    sig = sig.ch_defaults(_dry_run=False).ch_kinds(_dry_run=Sig.KEYWORD_ONLY)

    @sig
    def execute_commands(*args, **kwargs):
        _dry_run = kwargs.pop('_dry_run', False)
        commands = commands_template.format(
            **sig.kwargs_from_args_and_kwargs(args, kwargs)
        ).split('\n')
        n_commands = len(commands)
        for i, command in enumerate(commands, 1):
            print(f'\n({i}/{n_commands})$ {command}')
            if not _dry_run:
                output = execute_command(command)
                if output:
                    print(output)
                if step_by_step and i != n_commands:
                    input('TYPE ANY KEY TO CONTINUE')

    if name:
        execute_commands.__name__ = name

    return execute_commands

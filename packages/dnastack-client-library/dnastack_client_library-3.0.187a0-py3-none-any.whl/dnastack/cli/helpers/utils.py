from argparse import HelpFormatter
from contextlib import contextmanager

from traceback import print_exc

from copy import deepcopy

import click
import inspect
import json
import logging
import re
import sys
from click import Command, Context, UsageError, Option, Group
from pydantic import BaseModel
from typing import Any, List, Callable, Tuple, Mapping, Optional, Union, Dict, Type

from dnastack.common.logger import get_logger
from dnastack.feature_flags import in_global_debug_mode


####################
# Click Extensions #
####################
class MutuallyExclusiveOption(Option):
    """
    A click Option wrapper for sets of options where one but not both must be specified
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        original_help = kwargs.get("help", "")
        if self.mutually_exclusive:
            additional_help_text = "This is mutually exclusive with " \
                                   + " and ".join(sorted(self.mutually_exclusive)) + "."
            kwargs[
                "help"] = f"{original_help}. Note that {additional_help_text}" if original_help else additional_help_text
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx: click.Context, opts: Mapping[str, Any], args: List[str]) -> Tuple[
        Any, List[str]]:
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            raise UsageError(
                "Illegal usage: `{}` is mutually exclusive with "
                "arguments `{}`.".format(self.name, ", ".join(self.mutually_exclusive))
            )

        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)


class AliasedGroup(Group):
    """
    A click Group wrapper, enabling command shortcuts/aliases for the group and its subgroups
    """

    def __init__(self, *args, **kwargs):
        self.aliases = kwargs.pop('aliases', [])
        super(AliasedGroup, self).__init__(*args, **kwargs)
        self.sub_commands = {}
        self.sub_aliases = {}

    def add_command(self, cmd: Command, name: Optional[str] = None) -> None:
        super().add_command(cmd, name)
        if hasattr(cmd, 'aliases'):
            self.sub_commands[cmd.name] = cmd.aliases
            for sub_alias in cmd.aliases:
                self.sub_aliases[sub_alias] = cmd.name

    def resolve_alias(self, cmd_name: str) -> str:
        if cmd_name in self.sub_aliases:
            return self.sub_aliases[cmd_name]
        return cmd_name

    def get_command(self, ctx: Context, cmd_name: str) -> Optional[Command]:
        cmd_name = self.resolve_alias(cmd_name)
        command = super(AliasedGroup, self).get_command(ctx, cmd_name)
        if command:
            return command

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        rows = []

        sub_commands = self.list_commands(ctx)

        max_len = max(len(cmd) for cmd in sub_commands)
        limit = formatter.width - 6 - max_len

        for sub_command in sub_commands:
            cmd = self.get_command(ctx, sub_command)
            if cmd is None:
                continue
            if hasattr(cmd, 'hidden') and cmd.hidden:
                continue
            if sub_command in self.sub_commands:
                aliases = self.sub_commands[sub_command]
                if len(aliases) > 0:
                    aliases = ",".join(sorted(aliases))
                    sub_command = "{0} ({1})".format(sub_command, aliases)
            cmd_help = cmd.get_short_help_str(limit)
            rows.append((sub_command, cmd_help))

        if rows:
            with formatter.section('Commands'):
                formatter.write_dl(rows)

########################################
# Command and Specification Definition #
########################################


class ArgumentSpec(BaseModel):
    """
    Argument specification

    This is designed to use with @command where you want to customize how it automatically maps the callable's arguments
    as the command arguments/options.
    """
    name: str
    arg_names: Optional[List[str]]
    as_option: bool = None
    help: Optional[str]
    choices: Optional[List]
    ignored: bool = False
    nargs: Optional[Union[int, str]]
    type: Optional[Type] = None  # WARNING: This will override the parameter reflection.
    required: Optional[bool]  # WARNING: This will override the parameter reflection.

    # NOTE: the "type" and "default value" can be determined via the reflection if implemented.

    def get_argument_names(self) -> List[str]:
        if not self.arg_names:
            return self.convert_param_name_to_argument_names(self.name, self.as_option)
        else:
            return [*self.arg_names, self.name]

    @staticmethod
    def convert_param_name_to_argument_names(param_name: str, as_option: bool = False) -> List[str]:
        if as_option:
            return [f"--{re.sub(r'_', '-', param_name)}", param_name]
        else:
            return [param_name]


def command(command_group: Group,
            alternate_command_name: Optional[str] = None,
            specs: List[Union[ArgumentSpec, Dict[str, Any]]] = None,
            excluded_arguments: List[str] = None,
            setup_debug_enabled: bool = False,
            hidden: bool = False):
    """
    Set up a basic command and automatically configure CLI arguments or options based on the signature
    of the handler (given callable).

    :param command_group: the command group
    :param alternate_command_name: the alternate command name - by default, the command name is derived from the name
                                   of the annotated/decorated callable.
    :param specs: OVERRIDING argument/option specifications - by default, this decorator will automatically set any
                  callable's arguments as CLI in-line arguments.
    :param excluded_arguments: The list of callable's arguments to ignore from the autoconfiguration.
    """
    _logger = get_logger('@command', logging.DEBUG) if setup_debug_enabled else get_logger('@command', logging.WARNING)

    argument_specs = [(ArgumentSpec(**spec) if isinstance(spec, dict) else spec)
                      for spec in (specs or list())]

    argument_specs.extend([
        ArgumentSpec(
            name='no_auth',
            arg_names=['--no-auth'],
            as_option=True,
            help='Disable authentication',
            required=False,
        ),
        ArgumentSpec(
            name='endpoint_id',
            arg_names=['--endpoint-id'],
            as_option=True,
            help='Endpoint ID',
            required=False,
        ),
        # Deprecated
        ArgumentSpec(
            name='endpoint_url',
            arg_names=['--endpoint-url'],
            as_option=True,
            help='Endpoint URL',
            required=False,
        ),
    ])

    argument_spec_map: Dict[str, ArgumentSpec] = {spec.name: spec for spec in argument_specs}

    excluded_argument_names = excluded_arguments or list()
    for spec in argument_spec_map.values():
        if spec.ignored:
            excluded_argument_names.append(spec.name)

    def decorator(handler: Callable):
        command_name = alternate_command_name if alternate_command_name else re.sub(r'_', '-', handler.__name__)

        _decorator_logger = get_logger(f'{_logger.name}/{command_name}', _logger.level)

        handler_signature = inspect.signature(handler)

        def handle_invocation(*args, **kwargs):
            if in_global_debug_mode:
                # In the debug mode, no error will be handled gracefully so that the developers can see the full detail.
                handler(*args, **kwargs)
            else:
                try:
                    handler(*args, **kwargs)
                except (IOError, TypeError, AttributeError, IndexError, KeyError):
                    click.secho('Unexpected programming error', fg='red', err=True)

                    print_exc()

                    sys.exit(1)
                except Exception as e:
                    error_type = type(e).__name__
                    # error_type = re.sub(r'([A-Z])', r' \1', error_type).strip()
                    # error_type = re.sub(r' Error$', r'', error_type).strip().capitalize()

                    click.secho(f'{error_type}: ', fg='red', bold=True, nl=False, err=True)
                    click.secho(e, fg='red', err=True)

                    sys.exit(1)

        handle_invocation.__doc__ = handler.__doc__

        command_obj = command_group.command(command_name, hidden=hidden)(handle_invocation)

        for param_name, param in handler_signature.parameters.items():
            if param_name in excluded_argument_names:
                continue

            _decorator_param_logger = get_logger(f'{_decorator_logger.name}/{param_name}', _logger.level)

            required = True
            default_value = None
            help_text = None
            nargs = None
            as_option = False
            as_flag = False

            _decorator_param_logger.debug(f'REFLECTED: {param}')

            annotation = param.annotation
            if annotation is None or annotation == inspect._empty:
                param_type = str
            elif inspect.isclass(annotation):
                param_type = annotation
            else:
                if sys.version_info >= (3, 8):
                    ##################################
                    # To support Python 3.8 or newer #
                    ##################################

                    from typing import get_origin, get_args
                    special_type = get_origin(annotation)
                    type_args = get_args(annotation)

                    _decorator_param_logger.debug(
                        f'SPECIAL TYPE: special_type = {special_type}, type_args = {type_args}')

                    if special_type is Union:
                        param_type = [t for t in type_args if t is not None][0]
                        required = type(None) not in type_args
                    elif special_type is list or special_type is List:
                        param_type = [t for t in type_args if t is not None][0]
                        required = True
                        nargs = -1
                    else:
                        raise RuntimeError(f'Programming Error: The type of parameter {param_name} ({annotation}) is '
                                           f'not supported by this decorator. Please contact the technical support.')
                else:
                    ##################################
                    # To support Python 3.7 or older #
                    ##################################

                    if str(annotation).startswith('typing.Union[') and 'NoneType' in str(annotation):
                        # To keep this simple, the union annotation with none type is assumed
                        # to be for an optional string argument. Python 3.8 code branch can
                        # detect the type better.
                        param_type = str
                        required = False
                    elif str(annotation) == 'typing.List[str]':
                        param_type = str
                        required = True
                        nargs = -1
                    else:
                        raise RuntimeError(f'Programming Error: The type of parameter {param_name} ({annotation}) is '
                                           f'not supported by @command. Please contact the technical support.')

            if param.default != inspect._empty:
                default_value = param.default
                required = False

            additional_specs = dict(type=param_type,
                                    required=required,
                                    default=default_value,
                                    show_default=not required and default_value is not None)

            if param_type is bool:
                as_option = True
                as_flag = True

            input_names = ArgumentSpec.convert_param_name_to_argument_names(param_name, as_option)

            # If the argument spec is defined, use the spec to override the reflection.
            if param_name in argument_spec_map:
                spec = argument_spec_map[param_name]

                _decorator_param_logger.debug(f'SPEC: {spec}')

                if spec.required is not None:
                    required = spec.required
                else:
                    spec.required = required

                if spec.as_option is not None:
                    as_option = spec.as_option
                else:
                    spec.as_option = as_option

                input_names = spec.get_argument_names()

                if spec.help:
                    help_text = spec.help

                if spec.choices:
                    additional_specs.update({
                        'type': click.Choice(spec.choices),
                        'show_choices': True,
                    })

                if spec.type:
                    additional_specs.update({
                        'type': spec.type
                    })

                if spec.nargs:
                    nargs = spec.nargs

                additional_specs.update({
                    'required': required,
                    'show_default': not required and default_value is not None,
                })
            # END: spec overriding

            if nargs is not None:
                additional_specs['nargs'] = nargs
                del additional_specs['default']

            if as_option:
                if help_text:
                    additional_specs['help'] = help_text

                if as_flag:
                    additional_specs['is_flag'] = True
                    additional_specs['required'] = False
                    additional_specs['show_default'] = False

                _decorator_param_logger.debug(f'SET: Option ({input_names}, {additional_specs})')
                click.option(*input_names, **additional_specs)(command_obj)
            else:
                del additional_specs['show_default']

                _decorator_param_logger.debug(f'SET: Argument ({input_names}, {additional_specs})')
                click.argument(*input_names, **additional_specs)(command_obj)
        # END: argument/option setup

        _decorator_logger.debug(f'Setup complete')

        return command_obj

    return decorator


#################
# Output Helper #
#################
def echo_header(title: str, bg: str = 'blue', fg: str = 'white'):
    text_length = 116

    lines = truncate_text(title, text_length)
    max_line_length = max([len(line) for line in lines])

    column_size = max_line_length + 4
    vertical_padding = ' ' * column_size

    print()
    click.secho(vertical_padding, bold=True, bg=bg, fg=fg)
    for line in lines:
        click.secho(f'  {line}{" " * (max_line_length - len(line))}  ', bold=True, bg=bg, fg=fg)
    click.secho(vertical_padding, bold=True, bg=bg, fg=fg)
    print()


def truncate_text(content: str, text_length: int) -> List[str]:
    blocks = content.split('\n')

    lines = []

    for block in blocks:
        lines.extend(truncate_paragraph(block, text_length))

    return lines


def truncate_paragraph(content: str, text_length: int) -> List[str]:
    words = content.split(r' ')
    words_in_one_line = []
    lines = []

    for word in words:
        if len(' '.join(words_in_one_line + [word])) > text_length:
            lines.append(' '.join(words_in_one_line))
            words_in_one_line.clear()

        words_in_one_line.append(word)

    if words_in_one_line:
        # Get the remainders.
        lines.append(' '.join(words_in_one_line))

    return lines


@contextmanager
def echo_progress(message: str, post_op_message: str, color: str):
    click.secho('>>> ' + message + ' ', nl=False)
    click.secho('IN PROGRESS', fg='yellow')
    try:
        yield
    except KeyboardInterrupt:
        click.secho('>>> ' + message + ' ', nl=False)
        click.secho('SKIPPED', fg='magenta')
    else:
        click.secho('>>> ' + message + ' ', nl=False)
        click.secho(post_op_message.upper(), fg=color)


def echo_dict_in_table(data: Dict[str, Any], left_padding_size: int = 0):
    displayed_data = {
        k: json.dumps(v)
        for k, v in data.items()
        if v is not None
    }

    key_length = max([len(k) for k in data.keys()])
    value_length = max([len(v) for v in displayed_data.values()])

    left_padding = ' ' * left_padding_size

    print()
    for k, v in displayed_data.items():
        key_padding_length = key_length - len(k)
        value_padding_length = value_length - len(v)
        print(f'{left_padding}{k}{" " * key_padding_length}{v}{" " * value_padding_length}')
    print()

def echo_list(title: str, items: List[str]):
    click.secho(title)
    for item in items:
        click.secho(f'  ● {item}')


def show_alternative_for_deprecated_command(alternative: Optional[str]):
    bg_color = 'yellow'
    fg_color = 'white'

    if alternative:
        echo_header(f'WARNING: Please use "{alternative}" instead.', bg_color, fg_color)
    else:
        echo_header('WARNING: No alternative to this command.', bg_color, fg_color)


def echo_result(prefix: Optional[str], result_color: str, result: str, message: str, emoji: Optional[str] = None):
    if prefix:
        click.secho(f'[{prefix}]', dim=True, nl=False, err=True, bold=True)

    click.secho(f' {emoji} {result.upper()} ' if emoji else f' {result.upper()} ',
                fg=result_color,
                nl=False,
                err=True)
    click.secho(message, err=True)
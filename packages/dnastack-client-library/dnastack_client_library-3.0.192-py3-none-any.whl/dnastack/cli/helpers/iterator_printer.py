from json import dumps as to_json_string

import click
from pydantic import BaseModel
from typing import TypeVar, Any, Iterable, Optional, Callable
from yaml import dump as to_yaml_string, SafeDumper

from dnastack.cli.helpers.exporter import normalize
from dnastack.feature_flags import in_interactive_shell, cli_show_list_item_index

I = TypeVar('I')
R = TypeVar('R')


def show_iterator(output_format: str,
                  iterator: Iterable[Any],
                  transform: Optional[Callable[[I], R]] = None,
                  limit: Optional[int] = None,
                  item_marker: Optional[Callable[[Any], Optional[str]]] = None) -> int:
    """ Display the result from the iterator """
    if output_format == OutputFormat.JSON:
        printer = JsonIteratorPrinter
    elif output_format == OutputFormat.YAML:
        printer = YamlIteratorPrinter
    else:
        raise ValueError(f'The given output format ({output_format}) is not available.')

    return printer.print(iterator, transform=transform, limit=limit, item_marker=item_marker)


class OutputFormat:
    JSON = 'json'
    YAML = 'yaml'
    CSV = 'csv'

    DEFAULT_FOR_RESOURCE = YAML
    DEFAULT_FOR_DATA = JSON


class JsonIteratorPrinter:
    @staticmethod
    def print(iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None) -> int:
        row_count = 0

        for row in iterator:
            if limit and row_count >= limit:
                break

            if row_count == 0:
                # First row
                click.echo('[')
            else:
                click.echo(',', nl=False)

                # Clean up from the previous iteration.
                if in_interactive_shell and item_marker:
                    marker = item_marker(row)
                    if marker:
                        click.secho(f' # {marker}', dim=True, err=True, nl=False)

                if in_interactive_shell and cli_show_list_item_index:
                    click.secho(f' # {row_count}', dim=True, err=True, nl=False)

                click.echo('')  # just a new line

            entry = transform(row) if transform else row
            click.echo(
                '\n'.join([
                    f'  {line}'
                    for line in to_json_string(normalize(entry), indent=2, sort_keys=True).split('\n')
                ]),
                nl=False)

            row_count += 1

        if row_count == 0:
            click.echo('[]')
        else:
            click.echo('\n]')

        return row_count


class YamlIteratorPrinter:
    @staticmethod
    def print(iterator: Iterable[Any],
              transform: Optional[Callable[[I], R]] = None,
              limit: Optional[int] = None,
              item_marker: Optional[Callable[[Any], Optional[str]]] = None) -> int:
        row_count = 0

        for row in iterator:
            if limit and row_count >= limit:
                break

            entry = transform(row) if transform else row
            normalized = normalize(entry)
            encoded = normalized if isinstance(normalized, str) else to_yaml_string(normalize(entry), Dumper=SafeDumper)

            click.echo('- ', nl=False)
            click.echo('\n'.join([
                    f'  {line}'
                    for line in encoded.split('\n')
                ]).strip(),
                nl=False)

            if in_interactive_shell and item_marker:
                marker = item_marker(row)
                if marker:
                    click.secho(f' # {marker}', dim=True, err=True, nl=False)

            if in_interactive_shell and cli_show_list_item_index:
                click.secho(f' # {row_count}', dim=True, err=True, nl=False)

            click.echo()

            row_count += 1

        if row_count == 0:
            click.echo('[]')

        return row_count

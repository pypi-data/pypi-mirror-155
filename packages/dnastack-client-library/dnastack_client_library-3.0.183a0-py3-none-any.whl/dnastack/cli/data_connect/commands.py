import click
from imagination import container
from typing import Optional

from dnastack.client.data_connect import DataConnectClient
from .helper import handle_query
from dnastack.cli.helpers.exporter import to_json
from dnastack.cli.helpers.utils import AliasedGroup, command, ArgumentSpec
from dnastack.cli.helpers.client_factory import ConfigurationBasedClientFactory


def _get(id: Optional[str] = None) -> DataConnectClient:
    factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
    return factory.get(DataConnectClient, id)


@click.group("data-connect", cls=AliasedGroup, aliases=["dataconnect", "dc"])
def data_connect_command_group():
    """ Interact with Data Connect Service """


@command(data_connect_command_group,
         'query',
         [
             ArgumentSpec(
                 name='output',
                 arg_names=['-o', '--output'],
                 as_option=True,
                 help="""
                    The path to the output file (Note: If the option is specified, there will be no output to stdout.)
                 """,
             ),
             ArgumentSpec(
                 name='format',
                 arg_names=["-f", "--format"],
                 as_option=True,
                 help='Output format',
                 choices=["json", "csv"],
             ),
             ArgumentSpec(
                 name='decimal_as',
                 arg_names=['--decimal-as'],
                 as_option=True,
                 help='The format of the decimal value',
                 choices=["string", "float"],
             ),
         ])
def data_connect_query(endpoint_id: Optional[str],
                       query: str,
                       output: Optional[str] = None,
                       format: str = "json",
                       decimal_as: str = 'string',
                       no_auth: bool = False):
    """ Perform a search query """
    return handle_query(_get(endpoint_id),
                        query,
                        format,
                        decimal_as,
                        output_file=output,
                        no_auth=no_auth)


@click.group("tables")
def table_command_group():
    """ Table API commands """


@command(table_command_group, 'list')
def list_tables(endpoint_id: Optional[str], no_auth: bool = False):
    """ List all accessible tables """
    click.echo(to_json([t.dict() for t in _get(endpoint_id).list_tables(no_auth=no_auth)]))


@command(table_command_group, 'get')
def get_table_info(endpoint_id: Optional[str], table_name: str, no_auth: bool = False):
    """ Get data from the given table """
    click.echo(to_json(_get(endpoint_id).table(table_name, no_auth=no_auth).info.dict()))


# noinspection PyTypeChecker
data_connect_command_group.add_command(table_command_group)

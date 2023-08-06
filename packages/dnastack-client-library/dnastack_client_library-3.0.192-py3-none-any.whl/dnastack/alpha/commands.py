import click


@click.group("alpha", hidden=True)
def alpha_command_group():
    """
    Interact with testing/unstable/experimental commands.

    Warning: Alpha commands are experimental. This command may change incompatibly.
    """

    click.secho("Warning: Alpha commands are experimental. This command may change incompatibly.",
                fg="yellow",
                err=True)

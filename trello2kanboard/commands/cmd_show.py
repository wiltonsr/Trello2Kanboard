import click
from trello2kanboard.cli import pass_context


@click.command('show', short_help='Show Trello project.')
@pass_context
def cli(ctx):
    """Extract project info from JSON file and print on screen."""
    print("show command")
    print(ctx.json_file)

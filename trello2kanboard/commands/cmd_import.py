import click
from trello2kanboard.cli import pass_context


@click.command('import', short_help='Import Trello project.')
@pass_context
def cli(ctx):
    """Record project info from JSON file on Kanboard."""
    ctx.log('Changed files: none')
    ctx.vlog('bla bla bla, debug info')

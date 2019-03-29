# -*- coding: utf-8 -*-
import click
import json
from trello2kanboard.cli import pass_context


@click.command('json', short_help='Show Trello JSON file.')
@click.option('-p/-n', '--pretty/--no-pretty', default=True,
              help='Format the JSON output.')
@pass_context
def cli(ctx, pretty):
    """Display JSON file on screen."""
    if pretty:
        formatted_json = json.dumps(ctx.json_file,
                                    indent=4,
                                    sort_keys=True)
        click.echo_via_pager(formatted_json)
    else:
        click.echo(ctx.json_file)

import click
import json
from trello2kanboard.cli import pass_context


@click.command('json', short_help='Show Trello JSON file.')
@click.option('-p/-n', '--pretty/--no-pretty', default=True,
              help='Format the JSON output.')
@pass_context
def cli(ctx, pretty):
    """Extract project info from JSON file and print on screen."""
    obj_json = None
    if pretty:
        formatted_json = json.dumps(ctx.json_file,
                                    indent=4,
                                    sort_keys=True)
        obj_json = formatted_json
    else:
        obj_json = ctx.json_file

    click.echo(obj_json)

# -*- coding: utf-8 -*-
import click
from trello2kanboard.cli import pass_context
from .utils import print_line, parser_json


@click.command('show', short_help='Show Trello project.')
@pass_context
def cli(ctx):
    """Extract project info from JSON file and print on screen."""

    project = parser_json(ctx.json_file)

    print_line()
    click.echo(u'Project: {}.'.format(project.name))
    print_line()

    for x, column in enumerate(project.columns, start=1):
        click.echo(u'Column {}: {}.'.format(x, column.name))
        for y, task in enumerate(column.tasks, start=1):
            print(u'Task {}: {}.'.format(y, task.name))
        print_line()

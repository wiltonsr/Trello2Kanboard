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

    for w, column in enumerate(project.columns, start=1):
        click.echo(u'Column {}: {}.'.format(w, column.name))
        for x, task in enumerate(column.tasks, start=1):
            print(u'Task {}: {}.'.format(x, task.name))
            for y, subtask in enumerate(task.subtasks, start=1):
                print(u'Subtask {}: {}.'.format(y, subtask.content))
            for z, comment in enumerate(task.comments, start=1):
                print(u'Comment {}: {}.'.format(z, comment.content))
        print_line()

    total_columns = len(project.columns)
    total_tasks = 0
    total_subtasks = 0
    total_comments = 0
    total_attachments = 0

    if total_columns >= 1:
        for c in project.columns:
            total_tasks += len(c.tasks)
            for t in c.tasks:
                total_subtasks += len(t.subtasks)
                total_comments += len(t.comments)
                total_attachments += len(t.attachments)

    click.echo(u'{} Columns Found.'.format(total_columns))
    click.echo(u'{} Tasks Found.'.format(total_tasks))
    click.echo(u'{} Subtask Found.'.format(total_subtasks))
    click.echo(u'{} Comments Found.'.format(total_comments))
    click.echo(u'{} Attachments Found.'.format(total_attachments))

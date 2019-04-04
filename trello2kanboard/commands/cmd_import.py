# -*- coding: utf-8 -*-
import click
import sys

from kanboard import Kanboard

from trello2kanboard.cli import pass_context
from .utils import print_line, parser_json


@click.command('import', short_help='Import Trello project.')
@click.option('--api-url', '-a',
              default='http://localhost/jsonrpc.php',
              help='URL address of the Kanboard API.',
              show_default=True)
@click.option('--username', '-u',
              default='jsonrpc',
              help='Username from Kanboard API.',
              show_default=True)
@click.option('--api-token', '-t', required=True,
              help='Token from Kanboard API.')
@pass_context
def cli(ctx, api_url, username, api_token):
    """Record project info from JSON file on Kanboard."""
    project = parser_json(ctx.json_file)

    kb = Kanboard(api_url, username, api_token)

    # Validating url, username and api_token provided.
    try:
        user = kb.get_me()
    except Exception as e:
        print(repr(e))
        print(u'Failed to get user: {}\nwith api token: \"{}\".'.format(
            username, api_token))
        sys.exit()

    # Creating project
    project_id = False
    while project_id is False:
        try:
            project_id = kb.create_project(owner_id=user['id'],
                                           name=project.name)
            print(u'Project {} successfully created.'.format(project_id))
            print(u'Project name: {}.'.format(project.name))
            print_line()
        except Exception as e:
            print(repr(e))
            print(u'Failed on Project creation. Trying again.')

    # Erasing default columns
    all_columns = False
    while all_columns is False:
        try:
            all_columns = kb.get_columns(project_id=project_id)
        except Exception as e:
            print(repr(e))
            print(u'Failed to get Projects columns. Trying again.')
    for c in all_columns:
        erased = False
        while erased is False:
            try:
                erased = kb.remove_column(column_id=c['id'])
                print(u'Default Column erased.')
            except Exception as e:
                print(repr(e))
                print(u'Failed to erase default Column. Trying again.')
    print_line()

    # Creating Columns
    for column in project.columns:
        column_id = False
        while column_id is False:
            try:
                column_id = kb.add_column(
                    project_id=project_id, title=column.name)
                print(u'Column {} successfully created.'.format(column_id))
                print(u'Column name: {}.'.format(column.name))
            except Exception as e:
                print(repr(e))
                print(u'Failed on Column creation. Trying again.')

        # Creating Tasks
        for task in column.tasks:
            task_id = False
            while task_id is False:
                try:
                    task_id = kb.create_task(title=task.name,
                                             project_id=project_id,
                                             column_id=column_id,
                                             date_due=task.date_due,
                                             description=task.desc)
                    print(u'Task {} successfully created.'.format(task_id))
                except Exception as e:
                    print(repr(e))
                    print(u'Failed on Task creation. Trying again.')

            # Creating Subtask
            for subtask in task.subtasks:
                subtask_id = False
                while subtask_id is False:
                    try:
                        subtask_id = kb.create_subtask(task_id=task_id,
                                                       title=subtask.content,
                                                       status=subtask.status)
                        print(u'Subtask {} successfully created.'.format(subtask_id))
                    except Exception as e:
                        print(repr(e))
                        print(u'Failed on Subtask creation. Trying again.')

            # Creating Comments
            for comment in task.comments:
                comment_id = False
                while comment_id is False:
                    try:
                        comment_id = kb.create_comment(task_id=task_id,
                                                       content=comment.content,
                                                       user_id=user['id'])
                        print(u'Comment {} successfully created.'.format(comment_id))
                    except Exception as e:
                        print(repr(e))
                        print(u'Failed on Comment creation. Trying again.')

        print_line()

    print(u'Project Imported successfully.')

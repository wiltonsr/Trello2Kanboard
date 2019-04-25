# -*- coding: utf-8 -*-
import click
import sys
import base64

from six.moves import urllib

from kanboard import Kanboard

from trello2kanboard.cli import pass_context
from .utils import print_line, parser_json


class InvalidUsername(Exception):
    pass


@click.command('import', short_help='Import Trello project.')
@click.option('--api-url', '-a',
              default='http://localhost/jsonrpc.php',
              help='URL address of the Kanboard API.',
              show_default=True)
@click.option('--project-owner', '-o',
              default=None,
              help='Username that will be the owner of the project.')
@click.option('--api-user', '-u',
              default='jsonrpc',
              help='Username from Kanboard API.',
              show_default=True)
@click.option('--api-token', '-t', required=True,
              help='Token from Kanboard API.')
@pass_context
def cli(ctx, api_url, api_user, api_token, project_owner):
    """Record project info from JSON file on Kanboard."""
    project = parser_json(ctx.json_file)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

    kb = Kanboard(api_url, api_user, api_token)

    # Validating url, username and api_token provided.
    user = None
    if api_user == 'jsonrpc':
        if project_owner is None:
            print(u'You must inform the Project Owner.')
            sys.exit()
        try:
            user = kb.get_user_by_name(username=project_owner)
            if user is not None:
                print(u'User {} - {} successfully connected.'.format(
                    user['username'], user['name']))
                print_line()
            else:
                raise InvalidUsername
        except InvalidUsername:
            print(u'Failed to get username: {}\nWith API user: {}\nAnd API token: \"{}\"\nOn address: {}.'.format(
                project_owner, api_user, api_token, api_url))
            sys.exit()
        except Exception as e:
            print(repr(e))
            sys.exit()
    else:
        try:
            user = kb.get_me()
            print(u'User {} - {} successfully connected.'.format(
                user['username'], user['name']))
            print_line()
        except Exception as e:
            print(repr(e))
            print(u'Failed to get user: {}\nWith api token: \"{}\"\nOn address: {}.'.format(
                api_user, api_token, api_url))
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

    # Adding user to project when using the jsonrpc API user
    if api_user == 'jsonrpc':
        user_added = False
        while user_added is False:
            user_added = kb.add_project_user(project_id=project_id,
                                             user_id=user['id'],
                                             role='project-manager')
            print(u'User {} successfully added to Project {}.'.format(
                user['username'], project_id))
            print_line()

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

            # Creating Attachments
            for attachment in task.attachments:
                attachment_id = False
                while attachment_id is False:
                    try:
                        req = urllib.request.Request(
                            url=attachment.url, headers=headers)
                        filedata = base64.b64encode(
                            urllib.request.urlopen(req).read()).decode('ascii')
                        attachment_id = kb.create_task_file(project_id=project_id,
                                                            task_id=task_id,
                                                            filename=attachment.filename,
                                                            blob=filedata)
                        print(u'Attachment {} successfully created.'.format(
                            attachment_id))
                    except Exception as e:
                        print(repr(e))
                        print(u'Failed on Attachment creation. Trying again.')

        print_line()

    print(u'Project Imported successfully.')

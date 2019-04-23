# -*- coding: utf-8 -*-
import os
import sys
import click

import dateutil.parser as parser

from .models import Project, Column, Task, Subtask, Comment, Attachment


def print_line(simbol='#'):
    rows, columns = os.popen('stty size', 'r').read().split()
    for i in range(int(columns)):
        click.echo('{}'.format(simbol), nl=False)


def parser_json(json_obj):
    try:
        project = Project(json_obj['name'])

        for l in json_obj['lists']:
            if l['closed'] is False:
                column = Column(name=l['name'], trello_id=l['id'])
                for c in json_obj['cards']:
                    task = Task(name=c['name'], trello_id=c['id'],
                                date_due=convert_date(c['due']), desc=c['desc'],
                                trello_column_id=c['idList'])
                    if column.trello_id == task.trello_column_id:
                        column.tasks.append(task)
                        for cl in json_obj['checklists']:
                            if cl['idCard'] == task.trello_id:
                                for ci in cl['checkItems']:
                                    if ci['state'] == 'incomplete':
                                        # Kanboard incomplete status value
                                        status = 0
                                    elif ci['state'] == 'complete':
                                        # Kanboard complete status value
                                        status = 2
                                    else:
                                        status = 0
                                    subtask = Subtask(content=ci['name'],
                                                      status=status)
                                    task.subtasks.append(subtask)
                        for a in json_obj['actions']:
                            if a['type'] == 'commentCard':
                                if a['data']['card']['id'] == task.trello_id:
                                    comment = Comment(
                                        content=a['data']['text'])
                                    task.comments.append(comment)
                        for at in c['attachments']:
                            if at['isUpload'] is True:
                                attachment = Attachment(
                                    filename=at['name'],
                                    url=at['url'])
                                task.attachments.append(attachment)
                project.columns.append(column)

        return project
    except Exception as e:
        print(repr(e))
        print(u'Invalid Trello JSON File.')
        print(
            u'JSON File must contain this keys: '
            'name, lists, cards, checklists and actions.')
        sys.exit()


def convert_date(str_date):
    if str_date is None:
        return None
    try:
        date_obj = parser.parse(str_date)
        return date_obj.strftime('%Y-%m-%d %H:%M')
    except Exception as e:
        print(repr(e))
        print('Impossible to convert {} to Kanboard date due format.'.format(str_date))
        sys.exit()

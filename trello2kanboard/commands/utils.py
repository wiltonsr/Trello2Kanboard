# -*- coding: utf-8 -*-
import os
import sys
import click

from .models import Project, Column, Task, Subtask, Comment


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
                                trello_column_id=c['idList'], desc=c['desc'])
                    if column.trello_id == task.trello_column_id:
                        column.tasks.append(task)
                        for cl in json_obj['checklists']:
                            if cl['idCard'] == task.trello_id:
                                for ci in cl['checkItems']:
                                    subtask = Subtask(content=ci['name'])
                                    task.subtasks.append(subtask)
                        for a in json_obj['actions']:
                            if a['type'] == 'commentCard':
                                if a['data']['list']['id'] == task.trello_id:
                                    comment = Comment(
                                        content=a['data']['text'])
                                    task.comments.append(comment)
                project.columns.append(column)

        return project
    except Exception as e:
        print(repr(e))
        print("Invalid Trello JSON File.")
        print(
            "JSON File must contain this keys: "
            "name, lists, cards, checklists and actions.")
        sys.exit()

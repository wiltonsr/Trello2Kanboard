# -*- coding: utf-8 -*-
import os
import sys
import click

from .models import Project, Column, Card


def print_line(simbol='#'):
    rows, columns = os.popen('stty size', 'r').read().split()
    for i in range(int(columns)):
        click.echo('{}'.format(simbol), nl=False)


def parser_json(json_obj):
    try:
        project = Project(json_obj['name'])

        for l in json_obj['lists']:
            if l['closed'] is False:
                column = Column(l['name'], l['id'])
                for c in json_obj['cards']:
                    card = Card(c['name'], c['idList'])
                    if column.trello_id == card.trello_column_id:
                        column.cards.append(card)
                project.columns.append(column)

        return project
    except Exception as e:
        print(repr(e))
        print("Invalid Trello JSON File.")
        print("JSON File must contain keys: name, lists and cards.")
        sys.exit()

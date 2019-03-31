# -*- coding: utf-8 -*-
import click
from trello2kanboard.cli import pass_context
from .utils import print_line


@click.command('show', short_help='Show Trello project.')
@pass_context
def cli(ctx):
    """Extract project info from JSON file and print on screen."""

    obj = ctx.json_file

    excluded_lists = 0

    click.echo('Project: {}.\n'.format(obj['name']))

    with click.progressbar(obj['lists'],
                           label='Reading Trello JSON Columns.') as list_bar:
        for l_id, trello_lists in enumerate(list_bar, start=1):
            l_id -= excluded_lists
            if trello_lists['closed'] is False:
                list_id = trello_lists['id']
                list_name = trello_lists['name']
                click.echo('Reading Column {}: {}.'.format(l_id, list_name))
                with click.progressbar(obj['cards'],
                                       label='Reading Trello JSON Cards.') as card_bar:
                    for c_id, trello_cards in enumerate(card_bar, start=1):
                        card_id = trello_cards['idList']
                        card_name = trello_cards['name']
                        if card_id == list_id:
                            click.echo('Reading Card {} from Column {}: {}.'.format(
                                c_id, l_id, card_name))
                print_line()
            else:
                excluded_lists += 1

    click.echo('\nProject {}: \nTotal of Columns: {}.\nTotal of Cards: {}.'.format(
        obj['name'], l_id, c_id))

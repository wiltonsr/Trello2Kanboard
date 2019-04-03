# -*- coding: utf-8 -*-
import click
import sys

from kanboard import Kanboard

from trello2kanboard.cli import pass_context
from .utils import parser_json


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

    try:
        user = kb.get_me()
    except Exception as e:
        print(repr(e))
        print('Failed to get user: {}\nwith api token: \"{}\".'.format(
            username, api_token))
        sys.exit()

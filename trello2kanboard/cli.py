# -*- coding: utf-8 -*-
import os
import json
import sys
import io
import re
import click


CONTEXT_SETTINGS = dict(auto_envvar_prefix='Trello2Kanboard',
                        help_option_names=['-h', '--help'])


class Context(object):

    def __init__(self):
        pass


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'commands'))


class Trello2KanboardCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('trello2kanboard.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


def print_version(ctx, param, value):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(abs_path, '__init__.py')
    with io.open(file_to_open, 'rt', encoding='utf8') as f:
        version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version '+version)
    ctx.exit()


@click.command(cls=Trello2KanboardCLI, context_settings=CONTEXT_SETTINGS)
@click.option('--json-file', '-j', required=True, type=click.File('rb'),
              help='Trello JSON file.')
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show version and exit.')
@pass_context
def cli(ctx, json_file):
    json_str = None

    with json_file as f:
        json_str = f.read().decode('UTF-8')

    try:
        obj_json = json.loads(json_str)
        ctx.json_file = obj_json
    except Exception as e:
        print(repr(e))
        print(u'Invalid JSON File.')
        sys.exit()
    """Simple Python Package for Importing Trello Projects from
    JSON Files Using the Kanboard API."""

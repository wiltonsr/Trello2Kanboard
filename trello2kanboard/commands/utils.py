# -*- coding: utf-8 -*-
import os
import click


def print_line(simbol='#'):
    rows, columns = os.popen('stty size', 'r').read().split()
    for i in range(int(columns)):
        click.echo('{}'.format(simbol), nl=False)

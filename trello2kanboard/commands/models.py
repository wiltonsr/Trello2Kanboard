# -*- coding: utf-8 -*-


class Project:
    def __init__(self, name, columns=None):
        self.name = name
        if columns is None:
            columns = []
        self.columns = columns


class Column:
    def __init__(self, name, trello_id, cards=None):
        self.name = name
        self.trello_id = trello_id
        if cards is None:
            cards = []
        self.cards = cards


class Card:
    def __init__(self, name, trello_column_id):
        self.name = name
        self.trello_column_id = trello_column_id

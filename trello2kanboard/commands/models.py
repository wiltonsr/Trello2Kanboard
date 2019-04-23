# -*- coding: utf-8 -*-


class Project:
    def __init__(self, name, columns=None):
        self.name = name
        if columns is None:
            columns = []
        self.columns = columns


class Column:
    def __init__(self, name, trello_id, tasks=None):
        self.name = name
        self.trello_id = trello_id
        if tasks is None:
            tasks = []
        self.tasks = tasks


class Task:
    def __init__(self, name, trello_id, trello_column_id,
                 date_due, desc=None, comments=None, subtasks=None,
                 attachments=None):
        self.name = name
        self.trello_id = trello_id
        self.trello_column_id = trello_column_id
        self.date_due = date_due
        if desc is None:
            desc = ''
        self.desc = desc
        if comments is None:
            comments = []
        self.comments = comments
        if subtasks is None:
            subtasks = []
        self.subtasks = subtasks
        if attachments is None:
            attachments = []
        self.attachments = attachments


class Subtask:
    def __init__(self, content, status):
        self.content = content
        self.status = status


class Comment:
    def __init__(self, content):
        self.content = content


class Attachment:
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url

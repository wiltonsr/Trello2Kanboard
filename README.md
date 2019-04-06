Trello2Kanboard
============

[![](https://img.shields.io/badge/python-3.4+-blue.svg)](https://www.python.org/download/releases/3.4.0/) [![](https://img.shields.io/badge/python-2.7+-blue.svg)](https://www.python.org/download/releases/2.7.2/) [![](https://img.shields.io/github/license/ResidentMario/missingno.svg)](https://github.com/wiltonsr/Flask-Toastr/blob/master/README.md)

Simple Python Package for Importing Trello Projects from JSON Files Using the [Kanboard API](https://docs.kanboard.org/en/latest/api/introduction.html).

Installing
----------

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
$ pip install Trello2Kanboard
```

Trello2Kanboard supports Python 2.7, 3.4 and newer.

A Simple Example of Import
----------------

Step 1: Access your Trello account and export your Trello Project to JSON:

Step 2: Access your Kanboard account and get/generate an API Token:

Step 3.1: Run application using the special user `jsonrpc` credentials:

    trello2kanboard --json-file /file/trello.json import \
      --api-url http://localhost/jsonrpc.php \
      --api-user jsonrpc \
      --api-token api-token-from-jsonrpc-kanboard-user \
      --project-owner kanboard-username

Step 3.2: Or just run using you own user credentials:

    trello2kanboard --json-file /file/trello.json import \
      --api-url http://localhost/jsonrpc.php \
      --api-user your-username \
      --api-token api-token-from-your-own-kanboard-user

You could also show information without Import
----------------
```bash
trello2kanboard --json-file /file/trello.json show
```

And display a pretty formated JSON on screen
----------------
```bash
trello2kanboard --json-file /file/trello.json json
```
Requirements
------------------
Trello2Kanboard depends from:

- [Kanboard Python Api Client](https://github.com/kanboard/python-api-client)
- [click](https://github.com/pallets/click)


Function Reference
------------------

Consult the [Kanboard API documentation](https://docs.kanboard.org/en/latest/api/introduction.html) for more details.

Development
-----------

This package is just a project to improve my python skills. Any suggestions or tips are welcome.

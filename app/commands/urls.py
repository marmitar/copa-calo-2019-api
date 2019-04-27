import click
import itertools as it
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound


defualt_methods = {'HEAD', 'OPTIONS'}


def describe_url(url):
    adapter = current_app.url_map.bind('localhost')
    rule, arguments = adapter.match(url, return_rule=True)

    endpoint = str(rule.endpoint)
    methods = ', '.join(rule.methods - defualt_methods)
    args = str(arguments)

    return endpoint, methods, args


def find_rules(order):
    rules = current_app.url_map.iter_rules()
    rules = sorted(rules, key=lambda rule: getattr(rule, order))

    return map(format_rule, rules)


def format_rule(rule):
    path = str(rule.rule)
    endpoint = str(rule.endpoint)
    methods = ', '.join(rule.methods - defualt_methods)

    return path, endpoint, methods


def max_lengths(table):
    def max_len(col):
        return max(len(row[col]) for row in table)

    cols = len(table[0])
    return list(map(max_len, range(cols)))


def formatted(rows, lengths):
    def format(column, length):
        return f'{column:{length}}'

    def format_row(row):
        return '  '.join(it.starmap(format, zip(row, lengths)))

    if isinstance(rows, tuple):
        return format_row(rows)

    return map(format_row, rows)


@click.command()
@click.option('--url', default=None,
              help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule',
              help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    headers = ('Rule', 'Endpoint', 'Methods', 'Arguments')

    if url:
        headers = headers[1:]
        rows = [describe_url(url)]

    else:
        headers = headers[:-1]
        rows = list(find_rules(order))

    lengths = max_lengths([headers] + rows)

    click.echo(formatted(headers, lengths))
    click.echo('-' * len(formatted(headers, lengths)))

    for row in formatted(rows, lengths):
        click.echo(row)

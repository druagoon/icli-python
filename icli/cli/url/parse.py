import json
from urllib.parse import (
    parse_qsl,
    urlparse,
)

import click
import pyperclip

from icli.cli.utils import print_table

from .cli import cli_url


def dye_green(text: str) -> str:
    return click.style(text, fg='green')


def dye_yellow(text: str) -> str:
    return click.style(text, fg='yellow')


def fmt_key(key: str) -> str:
    return f'{dye_green(key)}' if key else ''


@cli_url.command()
@click.option('--url', help='URL to be parsed')
@click.option('--clipboard', is_flag=True, help='Get url from clipboard')
@click.option('--parse-query', is_flag=True, help='Parse query to pretty')
def parse(url: str, clipboard: bool, parse_query: bool):
    """Parse url to components for human read."""
    if not url and clipboard:
        url = pyperclip.paste()
    if not url:
        raise click.MissingParameter(param_hint='url', param_type='option')
    pr = urlparse(url)
    if not pr.scheme:
        raise click.BadParameter(url, param_hint='url')
    parts = [
        ['URL', url],
        ['Scheme', pr.scheme],
        ['Host', pr.hostname],
        ['Port', pr.port or ''],
        ['Path', pr.path],
        ['Query', pr.query],
    ]
    if parse_query and pr.query:
        q = dict(parse_qsl(pr.query, True))
        query = json.dumps(q, indent=' ' * 4, sort_keys=True)
        parts.append(['', query])
    parts.append(['Fragment', pr.fragment])
    rows = [[fmt_key(k), v] for k, v in parts]
    headers = [dye_yellow('Key'), dye_yellow('Value')]
    print_table(rows, headers)

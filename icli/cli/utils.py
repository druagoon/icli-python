import click
import tabulate


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()


def print_simple(rows: list[list[str]], headers: list[str]) -> None:
    n_headers = len(headers)
    widths = []
    fields = []
    for i in range(n_headers):
        widths.append(max([len(x[i]) for x in rows] + [len(headers[i])]))
        fields.append('{{%d:<{%d}}}' % (i, i))
    line_fmt = '  '.join(fields)
    row_fmt = line_fmt.format(*widths)
    output = [row_fmt.format(*v).rstrip() for v in rows]
    output[:0] = [
        click.style(row_fmt.format(*headers).strip(), fg='green'),
        row_fmt.format(*('-' * width for width in widths)),
    ]
    click.echo('\n'.join(output))


def print_table(rows: list[list[str]], headers: list[str] = None, **kwargs) -> None:
    kwargs.setdefault('floatfmt', '.2f')
    kwargs.setdefault('tablefmt', 'grid')
    text = tabulate.tabulate(rows, headers=headers, **kwargs)
    click.echo(text)

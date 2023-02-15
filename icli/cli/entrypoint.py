import click

from icli.__about__ import __version__


@click.group(
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name='icli')
@click.pass_context
def icli(ctx: click.Context):
    """
    \b
      _  ____ _     ___
     (_)/ ___| |   |_ _|
     | | |   | |    | |
     | | |___| |___ | |
     |_|\____|_____|___|
    """
    pass


def main():
    return icli()


if __name__ == '__main__':
    main()

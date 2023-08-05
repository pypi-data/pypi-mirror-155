import click

from pr_st_cli import version
from pr_st_cli.commands.new.cli import new


@click.group()
@click.version_option(version=version)
def main():
    """
    pr-st-cli is a CLI package that helps create streamlit templates
    """
    pass


main.add_command(new)

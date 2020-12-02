# -*- coding: utf-8 -*-

"""Console script for snmp_adapter."""
import sys

import click

from snmp_adapter.experiments import snmp, xml, db


# From Click documentation
class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail("Too many matches: %s" % ", ".join(sorted(matches)))


# @click.group(cls=AliasedGroup, invoke_without_command=True)
# @click.pass_context
# def main(ctx):
#     if ctx.invoked_subcommand is None:
#         default()
#     pass


@click.group(cls=AliasedGroup)
def main():
    pass


# @main.command(hidden=True)
# def default():
#     """Console script for snmp_adapter."""
#     click.echo(
#         "Replace this message by putting your code into " "snmp_adapter.cli.main"
#     )
#     click.echo("See click documentation at http://click.pocoo.org/")
#     return 0


# ----------------------------------------------------------------------------


@main.group(
    "snmp", cls=AliasedGroup, chain=True, help="Experiments with SNMP protocol."
)
def snmp_group():
    pass


@snmp_group.command()
def quickstart():
    """PySNMP Quick Start Example"""
    snmp.quickstart()
    return 0


@snmp_group.command()
def common():
    """PySNMP Tutorial Common Operations Example"""
    snmp.common()
    return 0


@snmp_group.command()
def temperature():
    """One-Wire Temperature sensor on ControlByWeb X-410 module."""
    snmp.temperature()
    return 0


@snmp_group.command()
def rewrite():
    """PySNMP Tutorial Common Operations Example, rewritten."""
    snmp.rewrite()
    return 0


@snmp_group.command()
@click.option(
    "-a",
    "--address",
    default=snmp.DEFAULT_ADDRESSS,
    show_default=True,
    help="Interface IP address on which to listen.",
)
@click.option(
    "-p",
    "--port",
    default=snmp.DEFAULT_PORT,
    show_default=True,
    type=int,
    help="Port on which to listen.",
)
@click.option(
    "-c",
    "--community",
    default=snmp.DEFAULT_COMMUNITY,
    show_default=True,
    help="SNMP v1/v2 community to which to listen.",
)
@click.option(
    "-m",
    "--mib",
    "mibs",
    multiple=True,
    nargs=1,
    help="Load extra SNMP MIB(s) for nicer output.  Use multiple times to add multiple MIBs.",
)
def listen(address, port, community, mibs):
    """Listen to and SNMP trap and print events."""
    snmp.listen(address, port, community, snmp.DEFAULT_MIBS + mibs)
    return 0


# ----------------------------------------------------------------------------


@main.group("xml", cls=AliasedGroup, chain=True, help="Experiments with XML.")
def xml_group():
    pass


@xml_group.command()
@click.argument(
    "text",
    nargs=-1,
)
def words(text):
    """Output text as an XML document of individual words."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    xml.words(text)
    return 0


# ----------------------------------------------------------------------------


@main.group("db", cls=AliasedGroup, chain=True, help="Experiments with databases.")
def db_group():
    pass


@db_group.command()
@click.argument(
    "text",
    nargs=-1,
)
def sqlite(text):
    """Add the text as an XML document to an sqlite3 database."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    db.sqlite(text)
    return 0


@db_group.command()
@click.argument(
    "text",
    nargs=-1,
)
def litealchemy(text):
    """Add the text as an XML document to an sqlite3 database."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    db.litealchemy(text)
    return 0


@db_group.command()
@click.argument(
    "text",
    nargs=-1,
)
def ormlite(text):
    """Add the text as an XML document to an sqlite3 database."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    db.ormlite(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

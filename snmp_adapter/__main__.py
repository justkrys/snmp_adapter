# -*- coding: utf-8 -*-

"""Console script for snmp_adapter."""
import sys

import click

from snmp_adapter.experiments import snmp, xml, db


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


@click.group(cls=AliasedGroup, invoke_without_command=True, chain=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        default()


@main.command()
def default(args=None):
    """Console script for snmp_adapter."""
    click.echo(
        "Replace this message by putting your code into " "snmp_adapter.cli.main"
    )
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@main.command()
def quickstart():
    """PySNMP Quick Start Example"""
    snmp.quickstart()
    return 0


@main.command()
def common():
    """PySNMP Tutorial Common Operations Example"""
    snmp.common()
    return 0


@main.command()
def temperature():
    """One-Wire Temperature sensor on ControlByWeb X-410 module."""
    snmp.temperature()
    return 0


@main.command()
def rewrite():
    """PySNMP Tutorial Common Operations Example, rewritten."""
    snmp.rewrite()
    return 0


@main.command()
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


@main.command()
@click.argument(
    "text",
    nargs=-1,
)
def words(text):
    """Output text as an XML document of individual words."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    xml.words(text)
    return 0


@main.command()
@click.argument(
    "text",
    nargs=-1,
)
def sqlite(text):
    """Add the text as an XML document to an sqlite3 database."""
    text = " ".join(text) if text else 'We are the knights who say "NI"!'
    db.sqlite(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

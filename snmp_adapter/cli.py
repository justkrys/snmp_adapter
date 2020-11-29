# -*- coding: utf-8 -*-

"""Console script for snmp_adapter."""
import sys

import click

from snmp_adapter import snmp_adapter


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
    snmp_adapter.quickstart()
    return 0


@main.command()
def common():
    """PySNMP Tutorial Common Operations Example"""
    snmp_adapter.common()
    return 0


@main.command()
def temperature():
    """One-Wire Temperature sensor on ControlByWeb X-410 module."""
    snmp_adapter.temperature()
    return 0


@main.command()
def rewrite():
    """PySNMP Tutorial Common Operations Example, rewritten."""
    snmp_adapter.rewrite()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

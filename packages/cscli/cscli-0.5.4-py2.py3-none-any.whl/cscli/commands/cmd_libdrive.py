#!/usr/bin/env python3

import click

from cscli import MIN_DISK
from cscli.cli import pass_environment


@click.group("libdrive", short_help="manage library drives")
@pass_environment
def cli(ctx):
    """actions: find"""
    pass


"""
filtering": {
"arch": "exact",
"category": "exact",
"distribution": "exact",
"image_type": "exact",
"name": "exact",
"name__icontains": "exact",
"os": "exact",
"uuid": "exact",
"version": "exact"
"""


@cli.command()
@click.option("-a", "--arch", type=str)
@click.option("-c", "--category", type=str)
@click.option("-d", "--distribution", type=str)
@click.option("-i", "--image_type", click.Choice(["preinst", "install"]))
@click.option("-n", "--name", type=str)
@click.option("-o", "--os", type=str)
@click.option("-u", "--uuid", type=str)
@click.option("-v", "--version", type=str)
@pass_environment
def find(ctx, arch, category, distribution, image_type, name, os, uuid, version):
    """search for drive by attributes"""
    ctx.output(ctx.api.find_libdrive(ctx.drive_name))

#!/usr/bin/env python
"""
CLI entry module.
"""

import click
import importlib.util
import logging
import putiopy

from . import find_config

config = None
config_file = find_config()

if config_file:
    spec = importlib.util.spec_from_file_location("config", config_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)


@click.group()
@click.option(
    "--log-filename", default="blockout.log", help="Filename where log output is written"
)
@click.option("--log-level", help="Log level used")
@click.pass_context
def cli(
    ctx,
    log_filename="putio.log",
    log_level=None,
):
    ctx.ensure_object(dict)

    if config:
        if log_level is None:
            log_level = config.LOG_LEVEL

    logging.basicConfig(
        filename=log_filename,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=log_level,
    )


from . import commands


def main():
    cli(auto_envvar_prefix="BLOCKOUT", obj={})

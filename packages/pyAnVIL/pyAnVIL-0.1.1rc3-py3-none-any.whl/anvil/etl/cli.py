#!/usr/bin/env python3
import click
import logging

from extract import extract
from transform import transform
from load import load
from utility import utility
from anvil.etl import DEFAULT_OUTPUT_PATH
import pkg_resources
import yaml
import json

LOG_FORMAT = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
logger = logging.getLogger('etl_old-cli')


def read_config(path=None):
    """Read config, if no path, read from installed resource."""

    if not path:
        resource_package = __name__    
        path = 'utilities/config.yaml'  # Do not use os.path.join()
        config_file = pkg_resources.resource_stream(resource_package, path)    
    else:
        config_file = open(path) 

    config = yaml.load(config_file, Loader=yaml.SafeLoader)
    assert sorted(config.keys()) == ['consortiums', 'mapping'], f"Config missing expected keys. {config.keys()} "

    return config


@click.group()
@click.option('-v', '--verbose', count=True, default=2, help="Increase logging level 0-3.", show_default=True)
@click.option('--output_path', default=DEFAULT_OUTPUT_PATH, help='output path for working files and output.', show_default=True)
@click.option('--config_path', default=None, help='path to config file override.', show_default=True)
@click.pass_context
def cli(ctx, verbose, output_path,config_path):
    """ETL: extract from terra workspaces, google buckets and gen3; transform to FHIR; load to google  Healthcare API."""
    # ensure that ctx.obj exists and is a dict
    # set root logging
    if verbose == 0:
        logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
    elif verbose == 1:
        logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)
    elif verbose == 2:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    else:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['output_path'] = output_path
    ctx.obj['config'] =  read_config(config_path)


if __name__ == '__main__':
    cli.add_command(extract)
    cli.add_command(transform)
    cli.add_command(load)
    cli.add_command(utility)
    cli()

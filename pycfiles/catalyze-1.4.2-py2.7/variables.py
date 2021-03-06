# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/variables.py
# Compiled at: 2015-06-29 10:38:09
from __future__ import absolute_import
import json, itertools, click
from catalyze import cli, client, project, config, output
from catalyze.helpers import services, environment_variables

@cli.group('vars', short_help='Check/set/unset environment variables')
def vars_group():
    """Interacts with environment variables for the associated environment."""
    pass


@vars_group.command()
def list():
    """List all set variables."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    service = session.get('%s/v1/environments/%s/services/%s' % (config.paas_host, settings['environmentId'], settings['serviceId']), verify=True)
    variables = service['environmentVariables']
    for value, key in sorted(variables.items()):
        output.write('%s = %s' % (value, key))


@vars_group.command(short_help='Set or update a variable.')
@click.argument('variables', nargs=-1)
def set(variables):
    """Set or update one or more variables. Expects variables in the form <key>=<value>. Multiple variables can be set at once.

Variable changes will not take effect in the application until it is redeployed (via either a push or 'catalyze redeploy')."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    body = {}
    for var in variables:
        pieces = var.split('=', 1)
        if len(pieces) != 2:
            output.error('Expected argument form: <key>=<value>')
        else:
            body[pieces[0]] = pieces[1]

    environment_variables.set(session, settings['environmentId'], settings['serviceId'], body)


@vars_group.command()
@click.argument('variable')
def unset(variable):
    """Unset (delete) a variable.

Variable changes will not take effect in the application until it is redeployed (via either a push or 'catalyze redeploy')."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    environment_variables.unset(session, settings['environmentId'], settings['serviceId'], variable)
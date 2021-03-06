# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/attendant/configuration.py
# Compiled at: 2016-09-12 10:59:50
"""
Module for containing all required initialization logic.

It exposes a function that should ALWAYS be indepotent,
which means that it can be called one or possible multiple
times without creating fatal errors (other than those originated
by latency.)
"""
import sys, logging, logging.config, os
from os.path import join, isfile
from dotenv import load_dotenv

def loads(**kwargs):
    """Load and check all the necessary configuration options"""
    envPath = kwargs.pop('envPath', os.getcwd())
    env = kwargs.pop('envFile', '.env')
    ENVFILE_PATH = join(envPath, env)
    if isfile(ENVFILE_PATH):
        load_dotenv(ENVFILE_PATH)
    else:
        logging.error('No .env file found')
    logPath = kwargs.pop('logPath', os.getcwd())
    LOGFILE_PATH = join(logPath, 'logging.conf')
    if isfile(LOGFILE_PATH):
        logging.config.fileConfig(LOGFILE_PATH)
    else:
        logging.error('No logging.conf file found')
    productionOnly = set(kwargs.pop('productionOnly', {}))
    alwaysRequired = set(kwargs.pop('alwaysRequired', {}))
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)
    reqs = set()
    if os.getenv('SERVICE_ENV') == 'dev':
        required = reqs.union(alwaysRequired)
    else:
        required = reqs.union(productionOnly | alwaysRequired)
    real = set(os.environ.keys())
    bad = False
    diff = required - real
    if len(diff) > 0:
        bad = True
        logging.error('Missing environment variables: %s', (', ').join(diff))
    if bad:
        sys.exit(1)
    else:
        logging.info('All environment variables are valid.')
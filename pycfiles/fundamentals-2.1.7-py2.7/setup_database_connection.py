# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/mysql/setup_database_connection.py
# Compiled at: 2020-04-17 06:44:40
"""
*Given a yaml settings file containing database connection details, setup and return the db connector*

:Author:
    David Young
"""
from builtins import str
import sys, os, yaml
try:
    yaml.warnings({'YAMLLoadWarning': False})
except:
    pass

os.environ['TERM'] = 'vt100'
from fundamentals import tools

def setup_database_connection(pathToYamlFile):
    """*Start a database connection using settings in yaml file* 

    Given the location of a YAML dictionary containing database credientials, this function will setup and return the connection*

    **Key Arguments**

    - ``pathToYamlFile`` -- path to the YAML dictionary.
    

    **Return**

    - ``dbConn`` -- connection to the MySQL database.
    

    **Usage**

    The settings file should be in this form, with all keyword values set:

    ```yaml
    db: unit_tests
    host: localhost
    user: utuser
    password: utpass
    ```

    And here's how to generate the connection object:

    ```python
    from fundamentals.mysql import setup_database_connection
    dbConn = setup_database_connection(
        pathToYamlFile=pathToMyYamlFile
    )
    ```
    
    """
    import sys, logging, pymysql as ms
    try:
        logging.info('importing the yaml database connection dictionary from ' + pathToYamlFile)
        stream = open(pathToYamlFile, 'r')
        connDict = yaml.load(stream)
    except:
        logging.critical('could not load the connect dictionary from ' + pathToYamlFile)
        sys.exit(1)

    try:
        logging.info('connecting to the ' + connDict['db'] + ' database on ' + connDict['host'])
        dbConn = ms.connect(host=connDict['host'], user=connDict['user'], passwd=connDict['password'], db=connDict['db'], use_unicode=True, charset='utf8', local_infile=1, client_flag=ms.constants.CLIENT.MULTI_STATEMENTS, connect_timeout=36000)
        dbConn.autocommit(True)
    except Exception as e:
        logging.critical('could not connect to the ' + connDict['db'] + ' database on ' + connDict['host'] + ' : ' + str(e) + '\n')

    return dbConn
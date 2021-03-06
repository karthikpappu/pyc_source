# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/sql/utils.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 9908 bytes
"""
Created on Oct 2, 2012

@author: Nicklas Boerjesson
"""
from qal.dal.types import DB_POSTGRESQL, DB_MYSQL, DB_ORACLE, DB_DB2, DB_SQLSERVER, DB_SQLITE
from qal.common.listhelper import unenumerate

def check_for_param_content(_value):
    if _value[0:8] == '::Param=':
        return True
    else:
        return False


def none_as_sql(_value, _db_type, _none_value='', _error=None):
    """Raises an error or returns a value if blank"""
    if _value is not None:
        return _value.as_sql(_db_type)
    if _error is not None:
        raise Exception(_error)
    else:
        return _none_value


def check_not_null(_classname, _items):
    for _item in _items:
        if not _item[0]:
            raise Exception('Error in ' + _classname + ', ' + _item[1] + ' is not set.')


def error_on_blank(_value, _error):
    """Raises an error if blank"""
    if _value not in (None, ''):
        return _value
    raise Exception(_error)


def citate(_value, _db_type):
    """Adds citations when db_type is DB_POSTGRESQL"""
    if _db_type in (DB_POSTGRESQL, DB_DB2, DB_ORACLE):
        return '"' + str(_value) + '"'
    else:
        return _value


def comma_separate(_list, _db_type):
    """Convert a list of possible ParameterBase-descendants."""
    result = ''
    for currItem in _list:
        if result != '':
            result += ','
        if hasattr(currItem, 'as_sql'):
            result += currItem.as_sql(_db_type)
        else:
            result += citate(currItem, _db_type)

    return result


def parenthesise(_value):
    """Adds a parenthesis around a values."""
    return '(' + _value + ')'


def oracle_add_escape(_value, _escape_character):
    """Add the oracle escape ke_delimiteryword if nessesary."""
    if _escape_character not in ('', None):
        return _value + " ESCAPE '" + _escape_character + "'"
    else:
        return _value


def oracle_create_auto_increment(_table, _column):
    """Work around Oracle's silly unwillingness to support auto increment."""
    result = list()
    _new_seq = (_table.name + '_' + _column.name + '_seq')[0:29]
    result.append('')
    result[0] = 'CREATE SEQUENCE ' + _new_seq + _table.row_separator
    result[0] += 'start with 1' + _table.row_separator
    result[0] += 'increment by 1 ' + _table.row_separator
    result[0] += 'nomaxvalue'
    result.append('')
    result[1] = 'CREATE TRIGGER ' + ('tr_' + _table.name + '_' + _column.name)[0:29] + _table.row_separator
    result[1] += 'BEFORE INSERT ON "' + _table.name + '"' + _table.row_separator
    result[1] += 'FOR EACH ROW WHEN (new."' + _column.name + '" IS NULL) BEGIN' + _table.row_separator
    result[1] += 'SELECT ' + _new_seq + '.nextval INTO :new."' + _column.name + '" FROM dual;' + _table.row_separator
    result[1] += 'END;'
    return result


def add_operator(_index, _operator):
    """Adds a an operator if index > 0, used in loops when making conditions."""
    if _index > 0:
        return ' ' + _operator + ' '
    else:
        return ''


def add_comma(_index, _value):
    """Adds a comma if index > 0, used in loops when making lists."""
    if _index > 0:
        return ', ' + _value
    else:
        return _value


def add_comma_rs(_index, _value, _row_separator):
    """Adds a comma and row separator if index > 0, used in loops when making lists of references."""
    if _index > 0:
        return ',' + _row_separator + _value
    else:
        return _value


def curr_user(_db_type):
    """Returns a database-type specific (see dal_types) way of getting the current user."""
    if _db_type == DB_MYSQL:
        return '"Not supported by MySQL"'
    if _db_type == DB_POSTGRESQL:
        return 'session_user'
    if _db_type == DB_ORACLE:
        return 'USER'
    if _db_type == DB_DB2:
        return 'SESSION_USER'
    if _db_type == DB_SQLSERVER:
        return 'SUSER_SNAME()'
    if _db_type == DB_SQLITE:
        return '"Not supported by SQLite"'


def curr_datetime(_db_type):
    """Returns a database-type specific (see dal_types) way of getting the current date time."""
    if _db_type == DB_MYSQL:
        return 'CURRENT_TIMESTAMP'
    if _db_type == DB_POSTGRESQL:
        return 'current_timestamp'
    if _db_type == DB_ORACLE:
        return 'CURRENT_TIMESTAMP'
    if _db_type == DB_DB2:
        return 'CURRENT_TIMESTAMP'
    if _db_type == DB_SQLSERVER:
        return 'GETDATE()'
    if _db_type == DB_SQLITE:
        return "date('now')"


def db_specific_object_reference(_value, _db_type):
    """Qualifies an object reference in a database-type specific (see dal_types) way."""
    if _db_type == DB_MYSQL:
        return '`' + _value + '`'
    if _db_type in [DB_POSTGRESQL, DB_SQLITE]:
        return '"' + _value + '"'
    if _db_type == DB_ORACLE:
        return '"' + str(_value)[0:30] + '"'
    if _db_type == DB_DB2:
        return '"' + _value + '"'
    if _db_type == DB_SQLSERVER:
        return '[' + _value + ']'
    raise Exception('db_specific_object_reference: Invalid database type:' + str(_db_type))


def db_specific_datatype_parse_length(_value):
    if _value.find('(') > -1:
        _strlength = _value.split('(', 1)[1].rsplit(')', 1)[0]
        if _strlength.lower() != '' and _strlength.isdigit() is False:
            raise Exception('db_specific_datatype: Invalid syntax for datatype length:' + _value)
    else:
        _strlength = ''
    return _strlength


def db_specific_datatype(value, db_type):
    """
    Converts general DAL datatypes(as defined in sql_types) database-type specific (see dal_types) representations.

    @note: VARCHAR:
    For some reason, DB2 and Oracle doesn't support unspecified column lengths unless using BLOBs and cumbersome
    select constructs and casts. So DB2 will get 3100(max is 32704, but 4000 is the default page size for
    the table space so 3100 allows for the unspecified column to be at least usable.)
    Oracle is 4000 (limitations confirmed as of dec. 2012).
    """
    result = ''
    if value.lower() == 'integer':
        result = unenumerate(['INTEGER', 'integer', 'NUMBER', 'INT', 'int', 'INTEGER', 'INTEGER'], db_type)
    else:
        if value[:6].lower() == 'string' or value[:7].lower() == 'varchar':
            strlength = db_specific_datatype_parse_length(value)
            if strlength.lower() != '':
                result = unenumerate(['VARCHAR', 'varchar', 'VARCHAR2', 'VARCHAR', 'varchar', 'TEXT'], db_type)
                result += parenthesise(db_specific_datatype_parse_length(value))
            else:
                result = unenumerate(['TEXT', 'varchar', 'VARCHAR2(4000)', 'VARCHAR(3100)', 'varchar(max)', 'TEXT'], db_type)
        else:
            if value.lower() == 'float':
                result = unenumerate(['DOUBLE', 'double precision', 'FLOAT', 'Double', 'float', 'REAL'], db_type)
            else:
                if value.lower() == 'serial':
                    result = unenumerate([
                     'INTEGER AUTO_INCREMENT', 'serial', 'integer', 'INT GENERATED ALWAYS AS IDENTITY', 'int IDENTITY(1,1)', 'INTEGER PRIMARY KEY AUTOINCREMENT'], db_type)
                else:
                    if value.lower() == 'timestamp':
                        result = unenumerate(['TIMESTAMP', 'timestamp', 'TIMESTAMP', 'TIMESTAMP', 'DATETIME', 'TEXT'], db_type)
                    else:
                        if value.lower() == 'datetime':
                            result = unenumerate(['DATETIME', 'timestamp', 'DATE', 'TIMESTAMP', 'DATETIME', 'TEXT'], db_type)
                        else:
                            if value.lower() == 'boolean':
                                result = unenumerate(['BOOL', 'boolean', 'NUMERIC(1)', 'DECIMAL(1)', 'BIT', 'INTEGER'], db_type)
                            else:
                                if value.lower() == 'blob':
                                    result = unenumerate(['BLOB', 'bytea', 'BLOB', 'BLOB', 'VARBINARY(MAX)', 'BLOB'], db_type)
                                else:
                                    result = value
    return result


def db_specific_operator(_operator, _db_type):
    """Makes PostgreSQL's LIKE operator case insensitive by uppercasing it."""
    if str.lower(_operator) == 'like' and _db_type == DB_POSTGRESQL:
        return 'ILIKE'
    else:
        return _operator


def make_operator(_operator, _double_pipe_c):
    """Handles concatenation operators."""
    if _operator == 'C':
        if _double_pipe_c:
            return '||'
        else:
            return '+'
    else:
        return _operator


def make_function(_name, _value):
    """Assembles an SQL function call."""
    return _name + parenthesise(_value)


def handle_temp_table_ref(_identifier, _db_type):
    """Removes the "#" in SQL Server temporary table references. """
    if len(_identifier) > 0 and _identifier[0] == '#' and _db_type not in [DB_SQLSERVER]:
        return _identifier[1:]
    else:
        return _identifier


def datatype_to_parameter(_db_type, _datatype):
    """Converts a python data type to the database-driver appropriate parameter substitution string"""
    if _db_type == DB_MYSQL:
        return '%s'
    if _datatype[:6].lower() == 'string' or _datatype[:7].lower() == 'varchar' or _datatype in ('timestamp',
                                                                                                'datetime',
                                                                                                'blob'):
        return '%s'
    if _datatype in ('float', 'integer'):
        return '%d'
    raise Exception('datatype_to_parameter, unsupported data_type: ' + str(_datatype))
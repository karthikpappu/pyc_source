# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/sqlalchemy_mate-project/sqlalchemy_mate/crud/selecting.py
# Compiled at: 2019-04-26 17:40:16
# Size of source mod 2**32: 2548 bytes
"""
This module provide utility functions for select operation.
"""
from sqlalchemy import select, func, Column

def count_row(engine, table):
    """
    Return number of rows in a table.

    Example::

        >>> count_row(engine, table_user)
        3

    **中文文档**

    返回一个表中的行数。
    """
    return engine.execute(select([func.count()]).select_from(table)).fetchone()[0]


def select_all(engine, table):
    """
    Select everything from a table.

    Example::

        >>> list(select_all(engine, table_user))
        [(1, "Alice"), (2, "Bob"), (3, "Cathy")]

    **中文文档**

    选取所有数据。
    """
    s = select([table])
    return engine.execute(s)


def select_single_column(engine, column):
    """
    Select data from single column.

    Example::

        >>> select_single_column(engine, table_user.c.id)
        [1, 2, 3]

        >>> select_single_column(engine, table_user.c.name)
        ["Alice", "Bob", "Cathy"]
    """
    s = select([column])
    return (column.name, [row[0] for row in engine.execute(s)])


def select_many_column(engine, *columns):
    """
    Select data from multiple columns.

    Example::

        >>> select_many_column(engine, table_user.c.id, table_user.c.name)

    :param columns: list of sqlalchemy.Column instance

    :returns headers: headers
    :returns data: list of row

    **中文文档**

    返回多列中的数据。
    """
    if isinstance(columns[0], Column):
        pass
    else:
        if isinstance(columns[0], (list, tuple)):
            columns = columns[0]
        s = select(columns)
        headers = [str(column) for column in columns]
        data = [tuple(row) for row in engine.execute(s)]
    return (
     headers, data)


def select_distinct_column(engine, *columns):
    """
    Select distinct column(columns).

    :returns: if single column, return list, if multiple column, return matrix.

    **中文文档**

    distinct语句的语法糖函数。
    """
    if isinstance(columns[0], Column):
        pass
    else:
        if isinstance(columns[0], (list, tuple)):
            columns = columns[0]
        s = select(columns).distinct()
        if len(columns) == 1:
            return [row[0] for row in engine.execute(s)]
        else:
            return [tuple(row) for row in engine.execute(s)]


def select_random(engine, table_or_columns, limit=5):
    """
    Randomly select some rows from table.
    """
    s = select(table_or_columns).order_by(func.random()).limit(limit)
    return engine.execute(s).fetchall()
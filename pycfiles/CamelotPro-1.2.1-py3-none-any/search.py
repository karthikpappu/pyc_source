# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/search.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nHelper functions to search through a collection of entities\n'
import logging
LOGGER = logging.getLogger('camelot.view.search')
import sqlalchemy.types
from sqlalchemy import sql, orm, schema
import camelot.types

def create_entity_search_query_decorator(admin, text):
    """create a query decorator to search through a collection of entities
    :param admin: the admin interface of the entity
    :param text: the text to search for
    :return: a function that can be applied to a query to make the query filter
    only the objects related to the requested text or None if no such decorator
    could be build
    """
    from camelot.view import utils
    if len(text.strip()):
        args = []
        joins = []

        def append_column(c, text, args):
            """add column c to the where clause using a clause that
            is relevant for that type of column"""
            arg = None
            if issubclass(c.type.__class__, camelot.types.Color):
                pass
            elif issubclass(c.type.__class__, camelot.types.File):
                pass
            elif issubclass(c.type.__class__, camelot.types.Code):
                codes = [ '%%%s%%' % s for s in text.split(c.type.separator) ]
                codes = codes + ['%'] * (len(c.type.parts) - len(codes))
                arg = c.like(codes)
            elif issubclass(c.type.__class__, camelot.types.VirtualAddress):
                arg = c.like(('%', '%' + text + '%'))
            elif issubclass(c.type.__class__, camelot.types.Image):
                pass
            elif issubclass(c.type.__class__, sqlalchemy.types.Integer):
                try:
                    arg = c == utils.int_from_string(text)
                except (Exception, utils.ParsingError):
                    pass

            elif issubclass(c.type.__class__, sqlalchemy.types.Date):
                try:
                    arg = c == utils.date_from_string(text)
                except (Exception, utils.ParsingError):
                    pass

            elif issubclass(c.type.__class__, sqlalchemy.types.Float):
                try:
                    float_value = utils.float_from_string(text)
                    precision = c.type.precision
                    if isinstance(precision, tuple):
                        precision = precision[1]
                    delta = 0.1 ** (precision or 0)
                    arg = sql.and_(c >= float_value - delta, c <= float_value + delta)
                except (Exception, utils.ParsingError):
                    pass

            elif issubclass(c.type.__class__, (sqlalchemy.types.String,)) or hasattr(c.type, 'impl') and issubclass(c.type.impl.__class__, (sqlalchemy.types.String,)):
                LOGGER.debug('look in column : %s' % c.name)
                arg = sql.operators.ilike_op(c, '%' + text + '%')
            if arg is not None:
                arg = sql.and_(c != None, arg)
                args.append(arg)
            return

        for t in text.split(' '):
            subexp = []
            if admin.search_all_fields:
                mapper = orm.class_mapper(admin.entity)
                for property in mapper.iterate_properties:
                    if isinstance(property, orm.properties.ColumnProperty):
                        for column in property.columns:
                            if isinstance(column, schema.Column):
                                append_column(column, t, subexp)

            for column_name in admin.list_search:
                path = column_name.split('.')
                target = admin.entity
                for path_segment in path:
                    mapper = orm.class_mapper(target)
                    property = mapper.get_property(path_segment)
                    if isinstance(property, orm.properties.PropertyLoader):
                        joins.append(getattr(target, path_segment))
                        target = property.mapper.class_
                    else:
                        append_column(property.columns[0], t, subexp)

            args.append(subexp)

        def create_query_decorator(joins, args):
            """Bind the join and args to a query decorator function"""

            def query_decorator(query):
                """The actual query decorator, call this function with a query
                as its first argument and it will return a query with a where
                clause for searching the resultset of the original query"""
                for join in joins:
                    query = query.outerjoin(join)

                subqueries = (sql.or_(*arg) for arg in args)
                query = query.filter(sql.and_(*subqueries))
                return query

            return query_decorator

        return create_query_decorator(joins, args)
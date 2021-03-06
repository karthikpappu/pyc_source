# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\util\misc.py
# Compiled at: 2020-02-14 01:16:14
# Size of source mod 2**32: 5430 bytes
from builtins import zip
import logging, pandas as pd
from activitysim.core import inject
from activitysim.core import pipeline
from activitysim.core.util import assign_in_place
logger = logging.getLogger(__name__)

def mapped_columns(*column_maps):
    """
    Given any number of column_maps
    return a list of unique column names
    """
    result = set()
    for column_map in column_maps:
        result |= set(column_map.values())

    return list(result)


def add_result_columns(base_dfname, from_df, prefix=''):
    dest_df = inject.get_table(base_dfname).to_frame()
    if prefix:
        from_df = from_df.copy()
        from_df.columns = [prefix + c for c in from_df.columns.values]
    assign_in_place(dest_df, from_df)
    pipeline.replace_table(base_dfname, dest_df)


def add_targets_to_data_dictionary(targets, prefix, spec):
    if spec is None:
        return
    spec_dict = {prefix + e[0]:e[1] for e in zip(spec.target, spec.description)}
    data_dict = inject.get_injectable('data_dictionary')
    for col in targets:
        dest_col_name = prefix + col
        description = spec_dict.get(dest_col_name, '-')
        data_dict[dest_col_name] = description


def add_summary_results(df, summary_column_names=None, prefix='', spec=None):
    if summary_column_names is not None:
        df = df[summary_column_names]
    if df.shape[0] > 1:
        df = pd.DataFrame(df.sum()).T
    add_targets_to_data_dictionary(df.columns, prefix, spec)
    add_result_columns('summary_results', df, prefix)


def missing_columns(table, expected_column_names):
    table_column_names = tuple(table.columns.values) + tuple(table.index.names)
    return list((c for c in expected_column_names if c not in table_column_names))


def extra_columns(table, expected_column_names):
    return list((c for c in table.columns.values if c not in expected_column_names))


def expect_columns(table, expected_column_names):
    missing_column_names = missing_columns(table, expected_column_names)
    extra_column_names = extra_columns(table, expected_column_names)
    for c in missing_column_names:
        print('expect_columns MISSING expected column %s' % c)

    for c in extra_column_names:
        print('expect_columns FOUND unexpected column %s' % c)

    if missing_column_names or extra_column_names:
        missing = ', '.join(missing_column_names)
        extra = ', '.join(extra_column_names)
        raise RuntimeError('expect_columns MISSING [%s] EXTRA:[%s]' % (missing, extra))
    return True


WILDCARD = '*'

def add_aggregate_results(results, spec, source='', zonal=True):
    if 'silos' not in spec.columns:
        raise RuntimeError('No Silo column in spec')
    elif zonal:
        all_silos = inject.get_injectable('coc_silos')
        zone_demographics = inject.get_table('zone_demographics').to_frame()
    else:
        all_silos = [
         'everybody']
        zone_demographics = None
    aggregate_results = inject.get_table('aggregate_results').to_frame()
    seen = set()
    for e in reversed(list(zip(spec.target, spec.silos, spec.description))):
        target, silos, description = e
        if target in seen:
            continue
        seen.add(target)
        if not target not in results.columns:
            if not silos:
                continue
            elif silos == WILDCARD:
                silo_names = all_silos
            else:
                silo_names = silos.split(';')
            new_row_index = len(aggregate_results)
            aggregate_results.loc[(new_row_index, 'Processor')] = source
            aggregate_results.loc[(new_row_index, 'Target')] = target
            aggregate_results.loc[(new_row_index, 'Description')] = description
            for silo in silo_names:
                if '=' in silo:
                    silo, pct_col = silo.split('=', 1)
                else:
                    pct_col = silo
                if pct_col == 'everybody':
                    aggregate_results.loc[(new_row_index, silo)] = results[target].sum()
                else:
                    aggregate_results.loc[(new_row_index, silo)] = (results[target] * zone_demographics[pct_col]).sum()

    pipeline.replace_table('aggregate_results', aggregate_results)
# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/flights.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2541 bytes
import pandas as pd
from sqlalchemy import DateTime
from superset import db
import superset.utils as utils
from .helpers import get_example_data, TBL

def load_flights(only_metadata=False, force=False):
    """Loading random time series data from a zip file in the repo"""
    tbl_name = 'flights'
    database = utils.get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            data = get_example_data('flight_data.csv.gz', make_bytes=True)
            pdf = pd.read_csv(data, encoding='latin-1')
            airports_bytes = get_example_data('airports.csv.gz', make_bytes=True)
            airports = pd.read_csv(airports_bytes, encoding='latin-1')
            airports = airports.set_index('IATA_CODE')
            pdf['ds'] = pdf.YEAR.map(str) + '-0' + pdf.MONTH.map(str) + '-0' + pdf.DAY.map(str)
            pdf.ds = pd.to_datetime(pdf.ds)
            del pdf['YEAR']
            del pdf['MONTH']
            del pdf['DAY']
            pdf = pdf.join(airports, on='ORIGIN_AIRPORT', rsuffix='_ORIG')
            pdf = pdf.join(airports, on='DESTINATION_AIRPORT', rsuffix='_DEST')
            pdf.to_sql(tbl_name,
              (database.get_sqla_engine()),
              if_exists='replace',
              chunksize=500,
              dtype={'ds': DateTime},
              index=False)
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'Random set of flights in the US'
    tbl.database = database
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    print('Done loading table!')
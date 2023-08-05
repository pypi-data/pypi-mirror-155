import logging
import os

from notedrive.sqlalchemy.base import BaseTable as _BaseTable
from notetool.secret import read_secret
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

uri = read_secret(cate1='notecoin', cate2='dataset', cate3='db_path')
uri = uri or f'sqlite:///{os.path.abspath(os.path.dirname(__file__))}/data/notecoin.db'

engine = create_engine(uri)
Base = declarative_base()
logging.info(f'uri:{uri}')


class BaseTable(_BaseTable):
    def __init__(self, table_name, *args, **kwargs):
        super(BaseTable, self).__init__(table_name, engine=engine, *args, **kwargs)

#
# class BaseTable:
#     def __init__(self, table_name, *args, **kwargs):
#         self.table_name = table_name
#         self.table: Table = None
#         meta.create_all(engine)
#
#     def insert(self, values, keys=None, *args, **kwargs):
#         meta.create_all(engine)
#         cols = [col.name for col in self.table.columns]
#         if isinstance(values, dict):
#             values = dict([(k, v) for k, v in values.items() if k in cols])
#         elif isinstance(values, list):
#             if isinstance(values[0], dict):
#                 values = [dict([(k, v) for k, v in item.items() if k in cols]) for item in values]
#             elif isinstance(values[0], list):
#                 values = [dict(zip(keys, item)) for item in values]
#
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             # code here...
#
#             if str(engine.url).startswith('sqlite'):
#                 ins = self.table.insert(values=values).prefix_with("OR IGNORE")
#             else:
#                 ins = self.table.insert(values=values).prefix_with("IGNORE")
#             engine.execute(ins)

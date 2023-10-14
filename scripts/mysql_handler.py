import sys
from typing import List, Union, Dict, Tuple
import os

import ujson

from helpers import dummy2db_logger


logger, extra_information = dummy2db_logger()

try:
    import mysql.connector
except ImportError:
    logger.error(
        'MySSQL Connector/Python not found, '
        'Download it from : http://dev.mysql.com/downloads/connector/python/', extra=extra_information)

    sys.exit(1)


class Dummy2dbMySqlHandler:
    def __init__(self, table_name: str = None, field_names: List[str] = [], data: Union[str, List[Dict], List[Tuple]] = None):
        self.table_name = table_name
        self.field_names = field_names
        self.data = data

        if table_name is None or not field_names or not data:
            logger.error("Table name or Field names or Data is/are not supplied",
                         extra=extra_information)
            sys.exit(1)

    def populate_table(self):
        payload = f"INSERT INTO {self.table_name}("

        for field_name in self.field_names:
            payload += f" {field_name},"

        payload = payload[:-1]
        payload += f" ) VALUES ( %s, "

        for i in range(0, len(self.field_names)):
            payload += "%s, "

        payload = payload[:-6] + " )"

        multi_lines = []
        if isinstance(self.data, str):
            data = self.process_data(self.data)

        for i in range(0, len(data)):
            multi_lines.append(
                list(ujson.loads(ujson.dumps(data[i])).values()))

        return multi_lines

    def process_data(self, filename: str):
        '''loads a file based on file extension'''
        extensions = ('json',)

        if not self.get_file_extension(filename) in extensions:
            raise NotImplementedError()
        else:
            with open(filename, "r") as f:
                data = f.read()
            return ujson.loads(data)

    def get_file_extension(self, filename: str):
        '''Returns the file extension of a file'''
        root, extension = os.path.splitext(filename)
        return extension[1:]


a = Dummy2dbMySqlHandler("rest", ["id", "name", "dob"], "data/core_users.json")
print(a.populate_table())

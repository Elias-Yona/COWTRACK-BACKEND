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

    def operation(self):
        '''Creates an insert sttaement dynamically'''

        payload = f"INSERT INTO {self.table_name}("

        for field_name in self.field_names:
            payload += f" {field_name},"

        payload = payload[:-1]
        payload += f" ) VALUES ( %s, "

        for i in range(0, len(self.field_names)):
            payload += "%s, "

        payload = payload[:-6] + " )"

        return payload

    def populate_table_mysql_initiator(self, host, port, password, username, name):
        payload = self.operation()
        multi_lines = []

        if isinstance(self.data, str):
            data = self.process_data(self.data)

        for i in range(0, len(data)):
            multi_lines.append(
                list(ujson.loads(ujson.dumps(data[i])).values()))

        self.commit_transaction(host=host, port=port, password=password,
                                username=username, name=name, operation=payload, data=multi_lines)

    def commit_transaction(self, host: str = "127.0.0.1", port: int = 3306, password: str = "", username: str = "root", name=None, operation: str = None, data: Union[List[List], List[Tuple]] = []):
        conn, cursor = None, None

        if not name or not operation or not data:
            logger.error(
                "Database name or operation or data is missing!", extra=extra_information)
            sys.exit(1)
        else:
            db = name

        try:
            conn = mysql.connector.connect(
                user=username, host=host, port=port, password=password)
            cursor = conn.cursor()
            cursor.execute(f"USE {db}")
            cursor.executemany(operation, data)
            conn.commit()

            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(e, extra=extra_information)
        else:
            logger.info('Data was commited successfully!',
                        extra=extra_information)

    def process_data(self, filename: str):
        '''loads data as a stream'''
        extensions = ('json',)

        if not self.get_file_extension(filename) in extensions:
            raise NotImplementedError()
        else:
            try:
                with open(filename, "r") as f:
                    data = f.read()
                return ujson.loads(data)
            except FileNotFoundError:
                logger.error("File not found", extra=extra_information)

    def get_file_extension(self, filename: str):
        '''Returns the file extension of a file'''
        root, extension = os.path.splitext(filename)
        return extension[1:]

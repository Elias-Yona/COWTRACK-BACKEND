import sys
from typing import List

from helpers import dummy2db_logger


logger, extra_information = dummy2db_logger()


class Dummy2dbMySqlHandler:
    def __init__(self, table_name: str = None, field_names: List[str] = []):
        self.table_name = table_name
        self.field_names = field_names

        if table_name is None or not field_names:
            logger.error("Table name or Field names are not supplied",
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

        return payload


a = Dummy2dbMySqlHandler("rest", ["id", "name", "dob"])
print(a.populate_table())

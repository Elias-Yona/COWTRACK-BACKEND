import subprocess
import time
import os
import sys

import ujson
import django
from django.contrib.auth.hashers import make_password
from yaspin import yaspin
from tqdm import tqdm


from helpers import dummy2db_logger
from mysql_handler import Dummy2dbMySqlHandler


logger, extra_information = dummy2db_logger()


def _mysqld_process_checkpoint():
    '''checks if mysql is available. if not it starts one
    '''
    try:
        subprocess.check_output("pgrep mysqld", shell=True)
    except Exception:
        logger.warning(
            'Your mysql server is offline, dummy2db will try to launch it now!',
            extra=extra_information)

        process = subprocess.Popen(
            "mysqld", close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        process.wait()

        time.sleep(3)


class CustomDummy2dbMySqlHandler(Dummy2dbMySqlHandler):
    def populate_table_mysql_initiator(self, host, port, password, username, name):
        payload = self.operation()
        multi_lines = []

        with yaspin(text="Loading data", color="yellow") as spinner:
            data = self.process_data(self.data)
            spinner.write("✅ Done data loading")

        for i in tqdm(range(0, len(data))):
            multi_lines.append(
                list(ujson.loads(ujson.dumps(data[i])).values()))

        with yaspin(text="saving data", color="yellow") as spinner:
            self.commit_transaction(host=host, port=port, password=password,
                                    username=username, name=name, operation=payload, data=multi_lines)
            spinner.write("✅ Done saving data to the database")
            print("\n")


def main():
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..")))

    if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cowtrack.settings')

    django.setup()

    _mysqld_process_checkpoint()

    users_mysql_handler = CustomDummy2dbMySqlHandler(
        table_name="core_user",
        field_names=["id", "password", "last_login", "is_superuser", "username", "first_name", "last_name",
                     "email", "is_staff", "is_active", "date_joined"],
        data="data/core_users.json"
    )

    users_mysql_handler.populate_table_mysql_initiator(
        "127.0.0.1", 3306, "", "root", "cowtrack")


if __name__ == '__main__':
    main()

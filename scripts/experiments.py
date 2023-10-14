import subprocess
import time
import os
import sys
import threading

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
    def append_to_list(self, data, multi_lines):
        '''Adds lines to a list'''

        for i in tqdm(range(0, len(data))):
            if self.table_name == "core_user":
                data[i]["password"] = make_password(
                    data[i].get("password"))
            multi_lines.append(
                list(ujson.loads(ujson.dumps(data[i])).values()))

    def populate_table_mysql_initiator(self, host, port, password, username, name):
        payload = self.operation()
        multi_lines1 = []
        multi_lines2 = []
        multi_lines3 = []
        multi_lines4 = []
        multi_lines5 = []
        multi_lines6 = []
        multi_lines7 = []
        multi_lines8 = []
        multi_lines9 = []
        multi_lines10 = []

        with yaspin(text="Loading data", color="yellow") as spinner:
            data = self.process_data(self.data)

            lines_per_mini_list = len(data) // 10

            mini_list1 = data[:lines_per_mini_list]  # nopep8
            mini_list2 = data[lines_per_mini_list:2*lines_per_mini_list]  # nopep8
            mini_list3 = data[2*lines_per_mini_list:3*lines_per_mini_list]  # nopep8
            mini_list4 = data[3*lines_per_mini_list:4*lines_per_mini_list]  # nopep8
            mini_list5 = data[4*lines_per_mini_list:5*lines_per_mini_list]  # nopep8
            mini_list6 = data[5*lines_per_mini_list:6*lines_per_mini_list]  # nopep8
            mini_list7 = data[6*lines_per_mini_list:7*lines_per_mini_list]  # nopep8
            mini_list8 = data[7*lines_per_mini_list:9*lines_per_mini_list]  # nopep8
            mini_list9 = data[8*lines_per_mini_list:9*lines_per_mini_list]  # nopep8
            # mini_list10 = data[9*lines_per_mini_list:10*lines_per_mini_list]  # nopep8
            mini_list10 = data[9*lines_per_mini_list:]  # nopep8

            thread_A = threading.Thread(
                target=self.append_to_list, args=(mini_list1, multi_lines1))
            thread_B = threading.Thread(
                target=self.append_to_list, args=(mini_list2, multi_lines2))
            thread_C = threading.Thread(
                target=self.append_to_list, args=(mini_list3, multi_lines3))
            thread_D = threading.Thread(
                target=self.append_to_list, args=(mini_list4, multi_lines4))
            thread_E = threading.Thread(
                target=self.append_to_list, args=(mini_list5, multi_lines5))
            thread_F = threading.Thread(
                target=self.append_to_list, args=(mini_list6, multi_lines6))
            thread_G = threading.Thread(
                target=self.append_to_list, args=(mini_list7, multi_lines7))
            thread_H = threading.Thread(
                target=self.append_to_list, args=(mini_list8, multi_lines8))
            thread_I = threading.Thread(
                target=self.append_to_list, args=(mini_list9, multi_lines9))
            thread_J = threading.Thread(
                target=self.append_to_list, args=(mini_list10, multi_lines10))

            thread_A.start()
            thread_B.start()
            thread_C.start()
            thread_D.start()
            thread_E.start()
            thread_F.start()
            thread_G.start()
            thread_H.start()
            thread_I.start()
            thread_J.start()

            thread_A.join()
            thread_B.join()
            thread_C.join()
            thread_D.join()
            thread_E.join()
            thread_F.join()
            thread_G.join()
            thread_H.join()
            thread_I.join()
            thread_J.join()

            spinner.write("✅ Done data loading")

        final_data = multi_lines1 + multi_lines2 + \
            multi_lines3 + multi_lines4 + multi_lines5 + multi_lines6 + multi_lines7 + \
            multi_lines8 + multi_lines9 + multi_lines10

        with yaspin(text="saving data", color="yellow") as spinner:
            self.commit_transaction(host=host, port=port, password=password,
                                    username=username, name=name, operation=payload, data=final_data)
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
        host="127.0.0.1", port=3306, password="", username="root", name="cowtrack")


if __name__ == '__main__':
    main()

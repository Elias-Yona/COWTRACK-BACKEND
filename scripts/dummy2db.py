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
            spinner.write(
                f"✅ Done saving {self.table_name} data to the database")
            print("\n")


def main():
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..")))

    if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'cowtrack.settings')

    django.setup()

    # _mysqld_process_checkpoint()

    tables = [
        {
            "table_name": "core_user",
            "field_names": ["id", "password", "last_login", "is_superuser", "username", "first_name", "last_name",
                            "email", "is_staff", "is_active", "date_joined"],
            "data": "data/core_users.json"
        },
        {
            "table_name": "salesmetrics_customer",
            "field_names": ["customer_id", "phone_number", "kra_pin", "contact_person", "address", "user_id"],
            "data": "data/salesmetrics_customers.json"
        },
        {
            "table_name": "salesmetrics_manager",
            "field_names": ["manager_id", "phone_number", "user_id"],
            "data": "data/salesmetrics_managers.json"
        },
        {
            "table_name": "salesmetrics_supervisor",
            "field_names": ["supervisor_id", "phone_number", "user_id"],
            "data": "data/salesmetrics_supervisors.json"
        },
        {
            "table_name": "salesmetrics_salesperson",
            "field_names": ["sales_person_id", "phone_number", "user_id"],
            "data": "data/salesmetrics_managers.json"
        },

        {
            "table_name": "salesmetrics_supplier",
            "field_names": ["supplier_id", "phone_number", "kra_pin", "contact_person", "notes", "user_id"],
            "data": "data/salesmetrics_suppliers.json"
        },
        {
            "table_name": "salesmetrics_location",
            "field_names": ["location_id", "latitude", "longitude", "address", "county"],
            "data": "data/salesmetrics_locations.json"
        },
        {
            "table_name": "salesmetrics_branch",
            "field_names": ["branch_id", "branch_name", "phone_number", "email", "opening_date", "location_id", "manager_id", "supervisor_id"],
            "data": "data/salesmetrics_branches.json"
        },
        {
            "table_name": "salesmetrics_productcategory",
            "field_names": ["category_id", "category_name"],
            "data": "data/salesmetrics_productcategories.json"
        },
        {
            "table_name": "salesmetrics_product",
            "field_names": ["product_id", "product_name", "cost_price_currency", "cost_price", "selling_price_currency", "selling_price", "is_serialized", "serial_number", "branch_id", "category_id"],
            "data": "data/salesmetrics_products.json"
        },
        {
            "table_name": "salesmetrics_paymentmethod",
            "field_names": ["payment_method_id", "method_name"],
            "data": "data/salesmetrics_paymentmethods.json"
        },
        {
            "table_name": "salesmetrics_cart",
            "field_names": ["cart_id", "number_of_items", "product_id"],
            "data": "data/salesmetrics_cart.json"
        },
        {
            "table_name": "salesmetrics_sale",
            "field_names": ["sale_id", "amount_currency", "amount", "transaction_date", "awarded_points", "cart_id", "customer_id", "payment_method_id", "sales_person_id"],
            "data": "data/salesmetrics_sales.json"
        },
        {
            "table_name": "salesmetrics_stock",
            "field_names": ["stock_id", "quantity_on_hand", "branch_id", "product_id"],
            "data": "data/salesmetrics_stock.json"
        },
    ]

    for table in tables:
        table_mysql_handler = CustomDummy2dbMySqlHandler(
            table_name=table.get("table_name"),
            field_names=table.get("field_names"),
            data=table.get("data")
        )

        table_mysql_handler.populate_table_mysql_initiator(
            "127.0.0.1", 3306, "", "root", "cowtrack")


if __name__ == '__main__':
    main()

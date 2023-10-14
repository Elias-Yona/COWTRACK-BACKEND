from django.db import models
from django.conf import settings

from djmoney.models.fields import MoneyField


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    kra_pin = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class SalesPerson(models.Model):
    sales_person_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Supervisor(models.Model):
    supervisor_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Manager(models.Model):
    manager_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Supplier(models.Model):
    supplier_id = models.BigAutoField(primary_key=True)
    phone_number = models.CharField(max_length=15)
    kra_pin = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=15)
    notes = models.TextField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=16, null=True, blank=True)
    address = models.CharField(max_length=200)
    county = models.CharField(max_length=50)


class Branch(models.Model):
    branch_id = models.BigAutoField(primary_key=True)
    branch_name = models.CharField(max_length=50)
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True)
    manager = models.OneToOneField(
        Manager, on_delete=models.SET_NULL, null=True)
    supervisor = models.OneToOneField(
        Supervisor, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)
    opening_date = models.DateField(auto_now_add=True)


class ProductCategory(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    cost_price = MoneyField(
        max_digits=19, decimal_places=4, default_currency='KSH')
    selling_price = MoneyField(
        max_digits=19, decimal_places=4, default_currency='KSH')
    is_serialized = models.BooleanField(default=1)
    serial_number = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True)


class Stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True)
    quantity_on_hand = models.IntegerField()
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE)
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True)


class StockTransfer(models.Model):
    stock_transfer_id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)
    stock_transfer_from = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True, db_column="from", related_name="stock_transfer_from")
    stock_transfer_to = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True, db_column="to", related_name="stock_transfer_to")


class StockDistribution(models.Model):
    stock_distribution_id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    distribution_date = models.DateTimeField(auto_now_add=True)
    stock_distribution_from = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True, db_column="from", related_name="stock_distribution_from")
    stock_distribution_to = models.ForeignKey(
        Stock, on_delete=models.SET_NULL, null=True, db_column="to", related_name="stock_distribution_to")


class Cart(models.Model):
    cart_id = models.BigAutoField(primary_key=True)
    number_of_items = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)


class PaymentMethod(models.Model):
    payment_method_id = models.BigAutoField(primary_key=True)
    method_name = models.CharField(max_length=50)


class Sale(models.Model):
    sale_id = models.BigAutoField(primary_key=True)
    amount = MoneyField(
        max_digits=19, decimal_places=4, default_currency='KSH')
    transaction_date = models.DateTimeField(auto_now_add=True)
    awarded_points = models.IntegerField()
    sales_person = models.ForeignKey(
        SalesPerson, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True)

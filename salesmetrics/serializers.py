from rest_framework import serializers

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product, Stock,
                     StockTransfer, StockDistribution)


class CustomUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'phone_number',
                  'kra_pin', 'contact_person', 'address', 'user']
    user = CustomUserSerializer()


class SalesPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPerson
        fields = ['sales_person_id', 'phone_number', 'user']
    user = CustomUserSerializer()


class SupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supervisor
        fields = ['supervisor_id', 'phone_number', 'user']
    user = CustomUserSerializer()


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['manager_id', 'phone_number', 'user']
    user = CustomUserSerializer()


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['supplier_id', 'phone_number',
                  'kra_pin', 'contact_person', 'notes', 'user']
    user = CustomUserSerializer()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'latitude',
                  'longitude', 'address', 'county']


class BranchSerializer(serializers.ModelSerializer):
    manager = serializers.SerializerMethodField('get_manager')
    supervisor = serializers.SerializerMethodField('get_supervisor')
    location = LocationSerializer()

    class Meta:
        model = Branch
        fields = ['branch_id', 'branch_name',
                  'location', 'manager', 'supervisor', 'phone_number', 'email', 'opening_date',]

    def get_manager(self, obj):
        if obj.manager:
            return {
                "phone_number": obj.manager.phone_number,
                "first_name": obj.manager.user.first_name,
                "last_name": obj.manager.user.last_name,
                "email": obj.manager.user.email,
                "date_joined": obj.manager.user.date_joined,
            }
        return None

    def get_supervisor(self, obj):
        if obj.manager:
            return {
                "phone_number": obj.supervisor.phone_number,
                "first_name": obj.manager.user.first_name,
                "last_name": obj.manager.user.last_name,
                "email": obj.manager.user.email,
                "date_joined": obj.manager.user.date_joined,
            }
        return None


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['category_id', 'category_name',]


class SimpleBranchSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    branch_name = serializers.CharField(max_length=50)
    location = LocationSerializer()
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=50)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')
    branch = SimpleBranchSerializer()

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'cost_price_currency', 'cost_price', 'selling_price_currency', 'selling_price', 'is_serialized',
                  'serial_number', 'category', 'branch']

    def get_category(self, obj):
        return {
            "id": obj.category.category_id,
            "name": obj.category.category_name
        }


class SimpleProductSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=50)


class SimpleBranchSerializer(serializers.Serializer):
    branch_name = serializers.CharField(max_length=50)


class StockSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    branch = SimpleBranchSerializer()

    class Meta:
        model = Stock
        fields = ['stock_id', 'quantity_on_hand', 'product', 'branch']


class StockTransferSerializer(serializers.ModelSerializer):
    stock_transfer_from = StockSerializer()
    stock_transfer_to = StockSerializer()
    transfer_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = StockTransfer
        fields = ['stock_transfer_id', 'quantity', 'transfer_date',
                  'stock_transfer_from', 'stock_transfer_to']


class StockDistributionSerializer(serializers.ModelSerializer):
    stock_distribution_from = StockSerializer()
    stock_distribution_to = StockSerializer()
    distribution_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = StockDistribution
        fields = ['stock_distribution_id', 'quantity', 'distribution_date',
                  'stock_distribution_from', 'stock_distribution_to']

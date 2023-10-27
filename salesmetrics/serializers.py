from decimal import Decimal

from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework.serializers import DecimalField
from django.contrib.auth import get_user_model


from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product, Stock,
                     StockTransfer, StockDistribution, Cart, PaymentMethod, Sale)


class CustomUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    is_superuser = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)


class CustomerSerializer(serializers.ModelSerializer):
    customer_image = serializers.SerializerMethodField('get_image')
    class Meta:
        model = Customer
        fields = ['customer_id', 'phone_number',
                  'kra_pin', 'contact_person', 'address', 'customer_image', 'user']
    user = CustomUserSerializer()

    def get_image(self, customer):
        return f"https://ui-avatars.com/api/?name=${customer.user.first_name}+${customer.user.last_name}"

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        username = user_data.get('username')
        if username:
            try:
                user, created = get_user_model().objects.get_or_create(**user_data)
            except IntegrityError:
                error_message = f"User with username '{username}' already exists."
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.create(user=user, **validated_data)
        return customer



    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            username = user_data.get('username')
            if username:
                user, created = get_user_model().objects.get_or_create(username=username)
                instance.user = user
                del user_data['username']
                del validated_data['kra_pin']

                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.email = user_data.get('email', user.email)
                user.address = user_data.get('address', user.address)


        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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


class SimpleProductCartSerializer(serializers.Serializer):
    product_name = serializers.CharField(max_length=50)
    selling_price = MoneyField(max_digits=19, decimal_places=2)
    serial_number = serializers.CharField(max_length=50)


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField('get_total_price')
    product = SimpleProductCartSerializer()

    class Meta:
        model = Cart
        fields = ['cart_id', 'number_of_items', 'product', 'total_price']

    def get_total_price(self, cart):
        return cart.number_of_items * cart.product.selling_price.amount


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['payment_method_id', 'method_name']


class SaleSerializer(serializers.ModelSerializer):
    sales_person = serializers.HyperlinkedRelatedField(
        view_name='salesperson-detail',
        queryset=SalesPerson.objects.all()
    )
    cart = serializers.HyperlinkedRelatedField(
        view_name='cart-detail',
        queryset=Cart.objects.all()
    )
    customer = serializers.HyperlinkedRelatedField(
        view_name='customer-detail',
        queryset=Customer.objects.all()
    )
    payment_method = PaymentMethodSerializer()
    balance = serializers.SerializerMethodField('get_balance')

    class Meta:
        model = Sale
        fields = ['sale_id', 'amount', 'transaction_date', 'awarded_points',
                  'sales_person', 'cart', 'customer', 'payment_method', 'balance']

    def get_balance(self, sale):
        cart_serializer = CartSerializer(sale.cart, context=self.context)
        total_price = cart_serializer.get_total_price(sale.cart)
        return sale.amount.amount - total_price

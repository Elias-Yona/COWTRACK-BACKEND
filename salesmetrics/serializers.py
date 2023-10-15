from rest_framework import serializers

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch)


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


class CustomManagerSerializer(serializers.Serializer):
    # user = CustomUserSerializer()
    manager = ManagerSerializer()

    # first_name = serializers.CharField(max_length=50, source='user.first_name')
    # last_name = serializers.CharField(max_length=50, source='user.last_name')
    # username = serializers.CharField(max_length=50, source='user.username')
    # email = serializers.EmailField(max_length=50, source='user.email')
    phone_number = serializers.CharField(
        max_length=15, source='manager.phone_number')


# class ManagerSerializer(serializers.Serializer):
#     user = CustomUserSerializer()
#     phone_number = serializers.CharField(max_length=15)


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

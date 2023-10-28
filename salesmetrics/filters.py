from django_filters.rest_framework import FilterSet
from .models import Customer, Manager, SalesPerson, Supervisor, Supplier


class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = {
            'user__date_joined': ['lt', 'gt'],
        }


class ManagerFilter(FilterSet):
    class Meta:
        model = Manager
        fields = {
            'user__date_joined': ['lt', 'gt'],
        }


class SalesPersonFilter(FilterSet):
    class Meta:
        model = SalesPerson
        fields = {
            'user__date_joined': ['lt', 'gt'],
        }


class SupervisorFilter(FilterSet):
    class Meta:
        model = Supervisor
        fields = {
            'user__date_joined': ['lt', 'gt'],
        }


class SupplierFilter(FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'user__date_joined': ['lt', 'gt'],
        }

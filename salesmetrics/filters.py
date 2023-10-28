from django_filters.rest_framework import FilterSet
from .models import Customer, Manager


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
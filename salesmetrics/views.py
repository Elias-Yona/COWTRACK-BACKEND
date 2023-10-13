from django.conf import settings

from rest_framework.viewsets import ModelViewSet

from .models import (Customer, SalesPerson, Supervisor, Manager, Supplier)
from .serializers import (
    CustomerSerializer, SalesPersonSerializer, SupervisorSerializer, ManagerSerializer, SupplierSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SalesPersonViewSet(ModelViewSet):
    queryset = SalesPerson.objects.all()
    serializer_class = SalesPersonSerializer


class SupervisorViewSet(ModelViewSet):
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer


class ManagerViewSet(ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

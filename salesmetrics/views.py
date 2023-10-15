from django.conf import settings

from rest_framework.viewsets import ModelViewSet

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product,
                     Stock)
from .serializers import (
    CustomerSerializer, SalesPersonSerializer, SupervisorSerializer, ManagerSerializer,
    SupplierSerializer, LocationSerializer, BranchSerializer, ProductCategorySerializer,
    ProductSerializer, StockSerializer)


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


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all().select_related(
        "manager").select_related("supervisor").select_related("location")
    serializer_class = BranchSerializer


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related(
        "branch").select_related("category")
    serializer_class = ProductSerializer


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all().select_related(
        "product").select_related("branch")
    serializer_class = StockSerializer

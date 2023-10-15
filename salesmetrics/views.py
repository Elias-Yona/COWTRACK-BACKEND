from django.conf import settings

from rest_framework.viewsets import ModelViewSet

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product,
                     Stock, StockTransfer, StockDistribution, Cart, PaymentMethod, Sale)
from .serializers import (
    CustomerSerializer, SalesPersonSerializer, SupervisorSerializer, ManagerSerializer,
    SupplierSerializer, LocationSerializer, BranchSerializer, ProductCategorySerializer,
    ProductSerializer, StockSerializer, StockTransferSerializer, StockDistributionSerializer,
    CartSerializer, PaymentMethodSerializer, SaleSerializer)


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


class StockTransferViewSet(ModelViewSet):
    queryset = StockTransfer.objects.all().select_related(
        "stock_transfer_from").select_related("stock_transfer_to")
    serializer_class = StockTransferSerializer


class StockDistributionViewSet(ModelViewSet):
    queryset = StockDistribution.objects.all().select_related(
        "stock_distribution_from").select_related("stock_distribution_to")
    serializer_class = StockDistributionSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all().select_related("product")
    serializer_class = CartSerializer


class PaymentMethodViewSet(ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all().select_related("sales_person").select_related(
        "cart").select_related("customer").select_related("payment_method")
    serializer_class = SaleSerializer

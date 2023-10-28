from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product,
                     Stock, StockTransfer, StockDistribution, Cart, PaymentMethod, Sale)
from .serializers import (
    CustomerSerializer, SalesPersonSerializer, SupervisorSerializer, ManagerSerializer,
    SupplierSerializer, LocationSerializer, BranchSerializer, ProductCategorySerializer,
    ProductSerializer, StockSerializer, StockTransferSerializer, StockDistributionSerializer,
    CartSerializer, PaymentMethodSerializer, SaleSerializer)
from .filters import CustomerFilter, ManagerFilter, SalesPersonFilter


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().select_related(
        "user").order_by('-user__date_joined')
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = CustomerFilter
    search_fields = ['phone_number', 'kra_pin',
                     'user__first_name', 'user__last_name']
    ordering_fields = ['user__date_joined',
                       'user__first_name', 'user__last_name']

    def update(self, request, *args, **kwargs):
        print(request.data)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            print(request.data)
            return Response(serializer.data)
        except Exception as e:
            # Capture the error and return it as a response
            error_message = str(e)
            print(request.data)
            print(e)
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class SalesPersonViewSet(ModelViewSet):
    queryset = SalesPerson.objects.all().select_related(
        "user").order_by('-user__date_joined')
    serializer_class = SalesPersonSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = SalesPersonFilter
    search_fields = ['phone_number',
                     'user__first_name', 'user__last_name']
    ordering_fields = ['user__date_joined',
                       'user__first_name', 'user__last_name']


class SupervisorViewSet(ModelViewSet):
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer


class ManagerViewSet(ModelViewSet):
    queryset = Manager.objects.all().all().select_related(
        "user").order_by('-user__date_joined')
    serializer_class = ManagerSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = ManagerFilter
    search_fields = ['phone_number',
                     'user__first_name', 'user__last_name']
    ordering_fields = ['user__date_joined',
                       'user__first_name', 'user__last_name']


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

from django.conf import settings

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from .models import (Customer, SalesPerson, Supervisor,
                     Manager, Supplier, Location, Branch, ProductCategory, Product,
                     Stock, StockTransfer, StockDistribution, Cart, PaymentMethod, Sale)
from .serializers import (
    CustomerSerializer, SalesPersonSerializer, SupervisorSerializer, ManagerSerializer,
    SupplierSerializer, LocationSerializer, BranchSerializer, ProductCategorySerializer,
    ProductSerializer, StockSerializer, StockTransferSerializer, StockDistributionSerializer,
    CartSerializer, PaymentMethodSerializer, SaleSerializer)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all().select_related("user").order_by('-user__date_joined')
    serializer_class = CustomerSerializer

    # def update(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, partial=False)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_update(serializer)
    #         return Response(serializer.data)
    #     except Exception as e:
    #         # Capture the error and return it as a response
    #         error_message = str(e)
    #         print(request.data)
    #         print(e)
    #         return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)



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

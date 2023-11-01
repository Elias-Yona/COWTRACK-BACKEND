from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('customers', views.CustomerViewSet)
router.register('salespersons', views.SalesPersonViewSet)
router.register('supervisors', views.SupervisorViewSet)
router.register('managers', views.ManagerViewSet)
router.register('suppliers', views.SupplierViewSet)
router.register('locations', views.LocationViewSet)
router.register('branches', views.BranchViewSet)
router.register('product-categories', views.ProductCategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('stock', views.StockViewSet)
router.register('stock-transfers', views.StockTransferViewSet)
router.register('stock-distributions', views.StockDistributionViewSet)
router.register('cart', views.CartViewSet)
router.register('payment-methods', views.PaymentMethodViewSet)
router.register('sales', views.SaleViewSet)
router.register("users", views.CustomUserViewSet)
router.register("supervisor-branch", views.SupervisorBranchViewSet)

supervisors_router = routers.NestedDefaultRouter(
    router, 'supervisors', lookup='supervisor')
supervisors_router.register(
    'branches', views.SupervisorBranchViewSet, basename='supervisor-branch')

urlpatterns = router.urls + supervisors_router.urls

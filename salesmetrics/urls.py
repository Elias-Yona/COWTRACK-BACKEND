from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('customers', views.CustomerViewSet)
router.register('salespersons', views.SalesPersonViewSet)
router.register('supervisors', views.SupervisorViewSet)

urlpatterns = router.urls

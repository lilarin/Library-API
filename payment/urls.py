from rest_framework import routers

from payment.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("", PaymentViewSet)

urlpatterns = router.urls

app_name = "payment"

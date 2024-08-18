from rest_framework.routers import DefaultRouter

from borrowing.views import BorrowingViewSet

router = DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = router.urls

app_name = "borrowing"

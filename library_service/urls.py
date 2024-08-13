from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/book/", include("book.urls", namespace="book")),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/borrowing/", include("borrowing.urls", namespace="borrowing")),
    path("api/payment/", include("payment.urls", namespace="payment")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger"
    ),
] + debug_toolbar_urls()

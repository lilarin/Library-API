from django.urls import path

from borrowing.views import (
    BorrowingListView,
    BorrowingDetailView,
    BorrowingCreateView
)

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing-list"),
    path("<int:pk>/", BorrowingDetailView.as_view(), name="borrowing-detail"),
    path("create/", BorrowingCreateView.as_view(), name="borrowing-create"),
]

app_name = "borrowing"

from django.urls import path

from borrowing.views import BorrowingCreateView, BorrowingListView

urlpatterns = [
    path("", BorrowingListView.as_view(), name="borrowing-list"),
    path("create/", BorrowingCreateView.as_view(), name="borrowing-create"),
]

app_name = "borrowing"

from django.urls import path

from borrowing.views import BorrowingCreateView


urlpatterns = [
    path("borrowings/", BorrowingCreateView.as_view(), name="borrowing-create"),
]

app_name = "borrowing"

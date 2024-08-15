from django.utils import timezone

from django.contrib import admin
from .models import Borrowing


class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "payment"
    )
    list_filter = (
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
        "book",
        "user"
    )
    search_fields = (
        "book__title",
        "user__email",
        "payment__session_id"
    )
    readonly_fields = ("payment",)

    fieldsets = (
        (None, {
            "fields": ("book", "user")
        }),
        ("Borrowing Dates", {
            "fields": (
                "borrow_date",
                "expected_return_date",
                "actual_return_date"
            )
        }),
        ("Payment Information", {
            "fields": ("payment",)
        }),
    )

    def mark_as_returned(self, request, queryset):
        updated = queryset.update(actual_return_date=timezone.now().date())
        self.message_user(
            request,
            f"{updated} borrowing(s) successfully marked as returned."
        )

    mark_as_returned.short_description = "Mark selected borrowings as Returned"


admin.site.register(Borrowing, BorrowingAdmin)

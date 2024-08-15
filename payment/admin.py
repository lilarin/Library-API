from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "payment_type",
        "money_to_pay",
        "session_url",
        "session_id"
    )
    list_filter = (
        "status",
        "payment_type"
    )
    search_fields = ("session_id",)
    readonly_fields = ("session_id",)

    fieldsets = (
        (None, {
            "fields": ("status", "payment_type", "money_to_pay")
        }),
        ("Payment Session Details", {
            "classes": ("collapse",),
            "fields": ("session_url", "session_id")
        }),
    )

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status=Payment.Status.PAID)
        self.message_user(
            request,
            f"{updated} payment(s) successfully marked as paid."
        )

    mark_as_paid.short_description = "Mark selected payments as Paid"


admin.site.register(Payment, PaymentAdmin)

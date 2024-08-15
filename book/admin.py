from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'cover',
        'inventory',
        'daily_fee'
    )
    list_filter = (
        'cover',
        'author'
    )
    search_fields = (
        'title',
        'author',
        'isbn'
    )
    readonly_fields = ('title',)

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'cover')
        }),
        ('Inventory and Pricing', {
            'fields': ('inventory', 'daily_fee')
        }),
    )

    def mark_all_out_of_stock(self, request, queryset):
        updated = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated} book(s) successfully marked as out of stock."
        )

    mark_all_out_of_stock.short_description = "Mark selected books as out of stock"


admin.site.register(Book, BookAdmin)

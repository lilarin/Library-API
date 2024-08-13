import django_filters

from borrowing.models import Borrowing


class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.ChoiceFilter(
        field_name="actual_return_date",
        method="filter_is_active",
        choices=((True, "Yes"), (False, "No")),
        label="Is Active",
    )
    user_id = django_filters.NumberFilter(field_name="user_id")

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    def filter_is_active(self, queryset, name, value):
        if value == "True":
            return queryset.filter(actual_return_date__isnull=True)
        elif value == "False":
            return queryset.filter(actual_return_date__isnull=False)
        return queryset

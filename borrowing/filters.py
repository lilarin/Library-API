from django_filters import FilterSet
from django_filters.rest_framework import filters

from borrowing.models import Borrowing


class BorrowingFilter(FilterSet):
    is_active = filters.ChoiceFilter(
        field_name="actual_return_date",
        method="filter_is_active",
        choices=((True, "Yes"), (False, "No")),
        label="Is Active",
    )
    user_id = filters.NumberFilter(field_name="user_id")

    class Meta:
        model = Borrowing
        fields = ["is_active", "user_id"]

    @staticmethod
    def filter_is_active(queryset, name, value):
        if value == "True":
            return queryset.filter(actual_return_date__isnull=True)
        elif value == "False":
            return queryset.filter(actual_return_date__isnull=False)
        return queryset

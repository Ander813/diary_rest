from django_filters.rest_framework.filterset import FilterSet
from django_filters.rest_framework import IsoDateTimeFilter
from .models import Record


class RecordsFilter(FilterSet):
    date_from = IsoDateTimeFilter(field_name="edit_date", lookup_expr="gte")
    date_to = IsoDateTimeFilter(field_name="edit_date", lookup_expr="lte")

    class Meta:
        model = Record
        fields = ['is_important']

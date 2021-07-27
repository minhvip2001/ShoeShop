from django.db.models import Q
import django_filters

class InvoiceFilterSet(django_filters.FilterSet):
    customer = django_filters.UUIDFilter(field_name="customer_id")
    code = django_filters.CharFilter(lookup_expr="icontains", field_name="code")
    created_at = django_filters.DateFromToRangeFilter()

class OrderItemFilterSet(django_filters.FilterSet):
    order = django_filters.UUIDFilter(field_name="order_id")
    created_at = django_filters.DateTimeFromToRangeFilter(field_name="created_at")
    customer = django_filters.UUIDFilter(field_name="order__customer_id")
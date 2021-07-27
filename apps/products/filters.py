import django_filters

class CategoryFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", field_name="name")
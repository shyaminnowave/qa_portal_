import django_filters
from django_filters import FilterSet, Filter
from apps.testcases.models import NatcoStatus


class NatcoStatusFilter(django_filters.FilterSet):

    jira_id = django_filters.CharFilter(field_name='test_case__jira_id', lookup_expr='iexact')
    natco = django_filters.CharFilter(field_name='natco__natco')
    language = django_filters.CharFilter(field_name='language__language_name', lookup_expr='iexact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    device = django_filters.CharFilter(field_name='device__name', lookup_expr='iexact')
    applicable = django_filters.BooleanFilter(field_name='applicable')

    class Meta:
        model = NatcoStatus
        fields = ['natco', 'language', 'device', 'jira_id', 'applicable']

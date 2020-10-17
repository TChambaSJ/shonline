import django_filters
from django_filters import DateFilter
from .models import *


class RequisitionFilter(django_filters.FilterSet):

    class Meta:
        model = Requisition
        fields = ['budget', 'requested_by', 'payee', 'status']
        
        


class LiquidationFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_submitted', lookup_expr='gte',)
    end_date = DateFilter(field_name='date_submitted', lookup_expr='lte')
    class Meta:
        model = Liquidation
        fields = ['requisition', 'compiled_by', 'status']

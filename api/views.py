import re
from collections import OrderedDict
from django.db.models import Sum, Count, F
from rest_framework import viewsets, mixins

from api.models import PerformanceMetrics
from rest_framework import filters
from rest_framework import response
from api.serializers import PerformanceMetricsSerializer, PerformanceMetricsListSerializer
from django_filters.rest_framework import DjangoFilterBackend


class AggregationByQueryParamMixin:

    @property
    def aggregations(self):
        aggregations = OrderedDict()
        aggregations["group_by"] = self.qs_group_by
        aggregations["count"] = self.qs_count
        aggregations["sum"] = self.qs_sum
        return aggregations

    def qs_group_by(self, queryset, query_params, *args, **kwargs):
        group_by = query_params.getlist('group_by', [])
        columns = set(query_params.getlist("column") + group_by)
        # exclude annotations from group_by values
        conflicts = set(query_params.getlist("sum", []) + query_params.getlist("count", []))
        queryset = queryset.values(*(columns-conflicts))
        return queryset

    def qs_sum(self, queryset, query_params, *args, **kwargs):
        fields_to_sum = query_params.getlist('sum', [])
        for field_to_sum in fields_to_sum:
            aggregate = {field_to_sum: Sum(field_to_sum)}
            queryset = queryset.annotate(**aggregate)
        return queryset

    def qs_count(self, queryset, query_params, *args, **kwargs):
        fields_to_count = query_params.getlist('count', [])
        for field_to_count in fields_to_count:
            aggregate = {field_to_count: Count(field_to_count)}
            queryset = queryset.annotate(**aggregate)
        return queryset


class PerformanceMetricApiView(AggregationByQueryParamMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    queryset = PerformanceMetrics.objects.all()
    serializer_class = PerformanceMetricsSerializer
    serializer_classes = {
        'detailed': PerformanceMetricsSerializer,
        'list': PerformanceMetricsListSerializer
    }
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = '__all__'
    filter_fields = {field.name: field.get_lookups().keys()
                     for field in PerformanceMetrics._meta.fields}

    def get_queryset(self):
        queryset = super(PerformanceMetricApiView, self).get_queryset()
        query_params = self.request.query_params
        # for every known aggregation, we rebuild queryset
        # by values from query_params
        queryset = self.qs_cpi(queryset=queryset, query_params=query_params)
        for aggregation, aggregation_func in self.aggregations.items():
            queryset = aggregation_func(queryset=queryset,
                                        query_params=query_params)
        return queryset

    def get_serializer_class(self):
        #  allow multiple serializers for retrieve and list actions
        try:
            return self.serializer_classes[self.action]
        except KeyError:
            return super(PerformanceMetricApiView, self).get_serializer_class()

    # calculation for cpi (special case)
    def qs_cpi(self, queryset, query_params, *args, **kwargs):
        if not query_params.get("get_cpi", False):
            return queryset
        return queryset.annotate(cpi=F("spend") / F("installs"))

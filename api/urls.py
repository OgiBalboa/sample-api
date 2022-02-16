from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PerformanceMetricApiView

router = DefaultRouter()
router.register(r'performance_metrics', PerformanceMetricApiView)

urlpatterns = [
    path(r'v1/', include(router.urls)),
]
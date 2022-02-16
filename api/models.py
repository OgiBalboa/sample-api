from django.db import models


class PerformanceMetrics(models.Model):
    date = models.DateTimeField()
    channel = models.CharField(max_length=50)
    country = models.CharField(max_length=4)
    os = models.CharField(max_length=7, choices=(('ios', 'ios'), ('android', 'android')))
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    installs = models.IntegerField()
    spend = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, null=False)

    objects = models.Manager()

    @property
    def cpi(self):
        return self.spend/self.installs
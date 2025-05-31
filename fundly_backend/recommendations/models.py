from django.db import models
from django.conf import settings

from finance.models import FinancialProduct

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendation')
    products = models.ManyToManyField(FinancialProduct, related_name='recommendation')
    created_at = models.DateTimeField(auto_now_add=True)
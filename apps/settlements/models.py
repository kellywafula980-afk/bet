from django.db import models
from django.conf import settings
from apps.betting.models import BetSlip

class Settlement(models.Model):
    betslip = models.ForeignKey(BetSlip, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_won = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    settled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Settlement for {self.betslip}"

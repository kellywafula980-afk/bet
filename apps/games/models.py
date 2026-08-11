from django.db import models
from django.conf import settings

class WheelSpin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wheel_spins')
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_settled = models.BooleanField(default=True)  # always settled immediately

    def __str__(self):
        return f"{self.user.username} - {self.win_amount} ({self.multiplier}x)"

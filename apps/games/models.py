from django.db import models
from django.conf import settings

class WheelSpin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wheel_spins')
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    multiplier = models.DecimalField(max_digits=5, decimal_places=2)
    win_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_settled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.win_amount} ({self.multiplier}x)"

class GameSetting(models.Model):
    # Demo mode forced outcomes for first three spins
    demo_first = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Multiplier for the FIRST demo spin (leave blank for random)"
    )
    demo_second = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Multiplier for the SECOND demo spin (leave blank for random)"
    )
    demo_third = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Multiplier for the THIRD demo spin (leave blank for random)"
    )
    # Live mode forced multiplier (single)
    live_forced_multiplier = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Set a multiplier for LIVE mode (e.g., 2.5). Leave blank for random."
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demo: {self.demo_first}, {self.demo_second}, {self.demo_third} | Live: {self.live_forced_multiplier}"

    class Meta:
        verbose_name = "Game Setting"
        verbose_name_plural = "Game Settings"

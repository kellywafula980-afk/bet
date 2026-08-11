from django.db import models
from django.conf import settings
from apps.sports.models import Match
from apps.odds.models import Odd

class BetSlip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='betslips')
    placed_at = models.DateTimeField(auto_now_add=True)
    stake = models.DecimalField(max_digits=10, decimal_places=2)
    potential_win = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_settled = models.BooleanField(default=False)
    settled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Slip #{self.id} - {self.user.username}"

class Bet(models.Model):
    betslip = models.ForeignKey(BetSlip, on_delete=models.CASCADE, related_name='bets')
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    odd = models.ForeignKey(Odd, on_delete=models.CASCADE)
    odds_at_time = models.DecimalField(max_digits=6, decimal_places=2)
    is_winner = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Bet on {self.match} at {self.odds_at_time}"
